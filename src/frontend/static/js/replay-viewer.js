var map, players, classes, data_frames;

var render_frames = [];
var cframe = 0;

var canvas, ctx;

var bmhp;

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

function render() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (var x in map) {
    // each render frame is [tanks, explosions, targets, shots, barriers]
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
    if (hp != -1) {
      ctx.fillStyle = "#3a3";
      ctx.beginPath();
      ctx.moveTo(sx - 75, sy - 5);
      ctx.lineTo(sx + 75, sy - 5);
      ctx.lineTo(sx + 75, sy + 5);
      ctx.lineTo(sx - 75, sy + 5);
      ctx.closePath();
      ctx.fill();
    }
  }
  for (var t of [0, 1]) {
    for (var tank of render_frames[cframe][0][t]) {
      var team = ["blue", "red"][t];
      var classid = classmap[tank.class];
      var path = "/static/images/" + team + "_" + classid + "_turret.png";
      var image = document.createElement("img");
      image.src = path;
      var scale = 0.25;
      var width = image.width * scale;
      var height = image.height * scale;
      ctx.save();
      ctx.translate(tank.x, tank.y);
      ctx.rotate(tank.barrel);
      ctx.drawImage(image, tank.x - width / 2, tank.y - height / 2, width, height);
      ctx.restore();
    }
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

    var indices = [[], []];

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
        indices[i].push(j++);
      }
    }

    // some extra frames so explosions can fade out at the end and such
    for (var frame = 0; frame < data_frames.length + 30; frame++) {
      if (frame < data_frames.length) {
        for (var i of [0, 1]) {
          for (var j in data_frames[frame][i]) {
            var state = tanks[i][indices[i][j]];
            var mod = data_frames[frame][i][j];
            if (mod === 0) {
              state.dead = 30;
              indices[i].splice(j, 1);
            } else {
              var [x, y, hp, shield, fire, cd, ability, statuses] = mod;
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
              state.shield = shield;
              if (fire != -1) {
                // TODO: compute shot
                state.barrel = fire;
              }
              state.cd = cd;
              if (ability != -1) {
                if (state.class == "repair") {
                  tanks[i][ability].healed = 30;
                } else if (state.class == "kamikaze") {
                  explosions.push([state.x, state.y, 30]);
                } else if (state.class == "mortar") {
                  var [tx, ty] = ability;
                  targets.push([30, tx, ty]);
                  explosions.push([30, tx, ty]);
                }
              }
              statuses.forEach(status => state[status] = true);
            }
          }
          if (frame === 0) bmhp = data_frames[frame][2];
        }
        render_frames.push(JSON.parse(JSON.stringify([tanks, explosions, targets, shots, barriers = data_frames[frame][2]])));
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
      } else {
        render_frames.push(JSON.parse(JSON.stringify([tanks, explosions, targets, shots, barriers])));
      }
    }

    render();
  });
})
