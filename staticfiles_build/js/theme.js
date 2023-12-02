$(document).ready(function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');
    var cssFile = "/backend/core/static/css"
    // var cssFile = "{% static 'css' %}"

    function swapStyles(sheet) {
        retorno = document.getElementById('mystylesheet').href = cssFile + '/' + sheet
        console.log(retorno)
        localStorage.setItem('theme', sheet)
        updateTheme(sheet)
    }

    function loadSettings() {
        var url = "{% url 'user_settings' %}"
        fetch(url, {
            method: 'GET',
            headers: {
                'Content-type': 'application/json'
            }
        })
            .then((response) => response.json())
            .then(function (data) {
                var theme = data.value;
                if (theme === 'light.css' || null) {
                    swapStyles('light.css')
                } else if (theme === 'dark.css') {
                    swapStyles('dark.css')
                }
            })
    }

    loadSettings()

    function updateTheme(theme) {
        var url = "{% url 'update_theme' %}"
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'theme': theme})
        })
    }
});