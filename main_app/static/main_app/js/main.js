$(document).ready(function () {
  // sidenav
  $(".sidenav").sidenav();
  // date picker
  $("#id_date").datepicker({
    format: "yyyy-mm-dd",
    defaultDate: new Date(),
    setDefaultDate: true,
  });
  // collapsibles
  $(".collapsible").collapsible();
  $(".dropdown-trigger").dropdown();
});

var selectEl = document.getElementById("id_nutrients");
M.FormSelect.init(selectEl);

var selectEl = document.getElementById("id_light");
M.FormSelect.init(selectEl);

var selectEl = document.getElementById("id_environment");
M.FormSelect.init(selectEl);

var selectEl = document.getElementById("id_watering_frequency");
M.FormSelect.init(selectEl);

var selectEl = document.getElementById("id_user");
M.FormSelect.init(selectEl);
