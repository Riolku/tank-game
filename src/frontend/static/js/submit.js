$(document).ready(() => {
  $("#switch").click(e => {
    if (e.currentTarget.children[0].children[0].checked) {
      $("#input-field").hide();
      $("#file-upload").show();
    } else {
      $("#input-field").show();
      $("#file-upload").hide();
    }
  });
});
