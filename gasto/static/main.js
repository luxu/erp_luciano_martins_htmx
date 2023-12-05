// auto_complete.js
$(function () {
   $('#id_name').autocomplete({
      delay: 600,
      minLength: 2,
      max: 10,
      scroll: true,
      source: function (request, response) {
          $.getJSON("/gasto/autocomplete/", request, function (data) {
              let suggestions = [];
              $.each(data, function (i, val) {
                  suggestions.push(val.name);
              });
              response(suggestions);
          });
      },
      search: function () {
          $("#loading").addClass("isloading");
      },
      response: function () {
          $("#loading").removeClass("isloading");
      }
   });
})