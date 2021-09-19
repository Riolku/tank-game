var map, players, classes, data_frames;

var render_frames = [];
var cframe = 0;
var playing = 0;
var repeating = false;

var speed_mul = 1;

function run() {
  if (cframe < render_frames.length - 1) {
    cframe += playing;
  } else if (playing) {
    if (repeating) {
      cframe = 0;
    } else {
      playing = 0;
      $("#pb").html("play_arrow");
    }
  }
  $("#timeline").val(cframe);
  setTimeout(run, 1000 / 24 / speed_mul);
}

run();

var canvas, ctx;

var bmhp, tmhp = [[], []];

var classmap = {
  "repair": "repair",
  "artillery": "artillery",
  "assassin": "assassin",
  "shield": "shield",
  "kamikaze": "sudoku",
  "scout": "scout",
  "mortar": "mortar",
  "hack": "hack_the_north"
};

function drawImage(ctx, path, scale, x, y, angle, alpha, gray) {
  if (alpha === 0) return;
  alpha = alpha || 1;
  gray = gray || false;
  var image = document.createElement("img");
  image.src = path;
  var width = image.width * scale;
  var height = image.height * scale;
  ctx.save();
  ctx.translate(x, y);
  ctx.rotate(angle + Math.PI / 2);
  ctx.globalAlpha = alpha;
  if (gray) ctx.filter = "grayscale(1)";
  ctx.drawImage(image, -width / 2, -height / 2, width, height);
  ctx.restore();
}

function render() {
  // each render frame is [tanks, explosions, targets, shots, barriers]
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  // render barriers
  for (var x in map) {
    var barrier = map[x];
    var hp = render_frames[cframe][4][x];
    ctx.fillStyle = hp == -1 ? "#000" : "#333";
    ctx.beginPath();
    ctx.moveTo(barrier[0][0], barrier[0][1]);
    var sx = 0, sy = 0, t = 0;
    for (var v of barrier) {
      ctx.lineTo(v[0], v[1]);
      sx += v[0];
      sy += v[1];
      t++;
    }
    sx /= t;
    sy /= t;
    ctx.closePath();
    ctx.fill();
    // render barrier HP bars
    if (hp != -1) {
      ctx.fillStyle = "#3a3";
      ctx.beginPath();
      ctx.moveTo(sx - 75, sy - 25);
      ctx.lineTo(sx - 75 + 150 * hp / bmhp[x], sy - 25);
      ctx.lineTo(sx - 75 + 150 * hp / bmhp[x], sy - 15);
      ctx.lineTo(sx - 75, sy - 15);
      ctx.closePath();
      ctx.fill();
    }
  }
  // render targeting reticles
  for (var t of render_frames[cframe][2]) {
    drawImage(ctx, "/static/images/mortar_target_icon.png", 0.2, t[1], t[2], 0, Math.max(0, t[0] - 15) / 30, false);
  }
  // render shots
  for (var t of render_frames[cframe][3]) {
    ctx.strokeStyle = "#000" + ["0", "3", "6", "9", "c", "f"][t[0]];
    ctx.beginPath();
    ctx.moveTo(t[1], t[2]);
    ctx.lineTo(t[1] + 1000 * Math.cos(t[3]), t[2] + 1000 * Math.sin(t[3]));
    ctx.stroke();
  }
  // render tanks
  for (var t of [0, 1]) {
    for (var i in render_frames[cframe][0][t]) {
      tank = render_frames[cframe][0][t][i];
      mhp = tmhp[t][i];
      var team = ["blue", "red"][t];
      var classid = classmap[tank.class];
      var scale = 0.15;
      var alpha = tank.dead == -1 ? tank.invisible ? 0.6 : 1 : tank.dead / 30;
      drawImage(ctx, "/static/images/" + team + "_tank.png", scale, tank.x, tank.y, tank.angle, alpha, tank.dead != -1);
      drawImage(ctx, "/static/images/" + team + "_" + classid + "_turret" + (tank.empowered ? "_empowered" : "") + ".png", scale, tank.x, tank.y, tank.barrel, alpha, tank.dead != -1);
      if (tank.dead != -1) continue;
      ctx.fillStyle = "#3a3";
      ctx.beginPath();
      ctx.moveTo(tank.x - 20, tank.y - 40);
      ctx.lineTo(tank.x - 20 + 40 * tank.hp / mhp, tank.y - 40);
      ctx.lineTo(tank.x - 20 + 40 * tank.hp / mhp, tank.y - 35);
      ctx.lineTo(tank.x - 20, tank.y - 35);
      ctx.closePath();
      ctx.fill();
    }
  }
  // render explosions
  for (var t of render_frames[cframe][1]) {
    drawImage(ctx, "/static/images/topdown_explosion.png", 0.2, t[1], t[2], 0, t[0] / 40, false);
  }
  requestAnimationFrame(render);
}

$(document).ready(() => {
  canvas = document.getElementById("canvas");
  ctx = canvas.getContext("2d");

  fetch("/match-data/" + $("#match").html()).then(r => r.text()).then(t => {
    // console.log(t);

    /*
      now we need to precompute all of the frames (because otherwise jumping/skipping will be qutie expensive)

      we need to consider the following things:
      - tank movement
      - tank abilities
      - explosion effects taking up multiple frames
      - target reticle from mortar
      - barrier and tank HP
      - cooldown display

      we need to store the following things at each frame:
      - tank positions
      - tank rotations
      - tank state (affected by abilities)
      - temporary display affects and transparency
      - barriers and HP values
      - tank HP and cooldown
    */

    [map, players, classes, data_frames] = JSON.parse(t);

    var tanks = [[], []];
    var targets = [];
    var explosions = [];
    var shots = [];
    var targets = [];
    var barriers;

    for (var i of [0, 1]) {
      var j = 0;
      for (var x of classes[i]) {
        tanks[i].push({
          "class": x,
          "x": -1,
          "y": -1,
          "angle": 0,
          "barrel": 0,
          "cd": 0,
          "hp": 0,
          "shield": 0,
          "empowered": false,
          "speedy": false,
          "invisible": false,
          "hacked": false,
          "healed": 0,
          "dead": -1
        });
      }
    }

    // some extra frames so explosions can fade out at the end and such
    for (var frame = 0; frame < data_frames.length + 30; frame++) {
      if (frame < data_frames.length) {
        for (var i of [0, 1]) {
          var remove = [];
          for (var j in data_frames[frame][i]) {
            var state = tanks[i][j];
            var mod = data_frames[frame][i][j];
            if (state.dead == -1) {
              var [x, y, hp, fire, cd, ability, statuses] = mod;
              if (state.x == -1 && state.y == -1) {
                state.x = x;
                state.y = y;
              }
              if (x != state.x || y != state.y) {
                state.angle = Math.atan2(y - state.y, x - state.x);
                state.x = x;
                state.y = y;
              }
              state.hp = hp;
              if (hp === 0) {
                state.dead = 30;
                continue;
              }
              if (frame === 0) tmhp[i][j] = hp;
              state.shield = false;
              if (fire != -1) {
                shots.push([5, x, y, fire]);
                state.barrel = fire;
              }
              state.cd = cd;
              if (ability != -1) {
                if (state.class == "repair") {
                  tanks[i][ability].healed = 30;
                } else if (state.class == "kamikaze") {
                  explosions.push([30, state.x, state.y]);
                } else if (state.class == "mortar") {
                  var [tx, ty] = ability;
                  targets.push([30, tx, ty]);
                  explosions.push([60, tx, ty]);
                }
              }
              for (var x of ["shielded", "empowered", "speedy", "invisible", "hacked"]) state[x] = false;
              statuses.forEach(status => state[status] = true);
            }
          }
          if (frame === 0) bmhp = data_frames[frame][2];
        }
        barriers = data_frames[frame][2];
      }
      render_frames.push(JSON.parse(JSON.stringify([tanks, explosions, targets, shots, barriers])));
      for (var i of [0, 1]) {
        for (var tank of tanks[i]) {
          if (tank.dead > 0) tank.dead--;
          if (tank.healed > 0) tank.healed--;
        }
        for (var q of [explosions, targets, shots]) {
          for (var j = 0; j < q.length; j++) {
            if (q[j][0] > 0) q[j][0]--;
            else {
              q.splice(j, 1);
              j--;
            }
          }
        }
      }
    }

    render();
  });
});

function restart() {
  cframe = 0;
}

function toggle() {
  if (!playing && cframe == render_frames.length - 1) cframe = 0;
  $("#pb").html(playing ? "play_arrow" : "pause");
  playing ^= 1;
}

function jump() {
  cframe += 10;
}

function rewind() {
  if (cframe > 0) cframe--;
}

function forward() {
  if (cframe < render_frames.length - 1) cframe++;
}

function checkbar() {
  cframe = parseInt($("#timeline").val());
}

function speed(x) {
  if (speed_mul + x > 0.2 && speed_mul + x <= 3) {
    speed_mul += x;
    $("#speed").html(Math.floor(speed_mul) + "." + Math.floor((speed_mul % 1) * 10) + "x");
  }
}

function repeat() {
  $("#rp").css("color", repeating ? "black" : "#0c0");
  repeating ^= true;
}
