$(document).ready(() => {
  var canvas = document.getElementById("canvas");
  var ctx = canvas.getContext("2d");

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

    var [map, players, classes, data_frames] = JSON.parse(t);
    var render_frames = [];
  });
})
