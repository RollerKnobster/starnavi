/**
 * Created by doorknob on 1/21/18.
 */

$('#comment-form').on('submit', function(event) {
    event.preventDefault();
    console.log('Form Submitted!');
    create_comment();
});

$('.comments').on('click', '.comment .delete-comment', function(event) {
    event.preventDefault();
    var comment_primary_key = $(this).attr('id').split('-')[2];
    console.log(comment_primary_key);
    delete_comment(comment_primary_key);
});

$('#datepicker').datepicker({
    minDate: -20,
    maxDate: '+1M +10D',
    showButtonPanel: true,
    changeMonth: true,
    changeYear: true,
    showOtherMonths: true,
    selectOtherMonths: true,
    showWeek: true,
    firstDay: 1,
    numberOfMonths: 2,
    showOn:"button",
    buttonImage: "http://jqueryui.com/demos/datepicker/images/calendar.gif",
    buttonImageOnly: true
});

$('#format').change(function () {
    $('#datepicker').datepicker('option', 'dateFormat', $(this).val());
});

$("#anim").change(function() {
  $("#datepicker").datepicker("option", "showAnim", $(this).val());
});

// var dates = $("#from, #to").datepicker({
//     defaultDate: "+1w",
//     changeMonth: true,
//     numberOfMonths: 2,
//     showOn:"button",
//     buttonImage: "http://jqueryui.com/demos/datepicker/images/calendar.gif",
//     buttonImageOnly: true
//     onSelect: function(selectedDate){
//     var option = this.id === "from" ? "minDate" : "maxDate",
//     instance = $( this ).data( "datepicker" ),
//     date = $.datepicker.parseDate(
//         instance.settings.dateFormat || $.datepicker._defaults.dateFormat,
//         selectedDate, instance.settings);
//     dates.not(this).datepicker("option", option, date);
//     }
// });

function create_comment() {
    console.log('create post is working');
    $.ajax({
        url: '.',
        type: 'POST',
        data: {
            name: $('#name').val(),
            email: $('#email').val(),
            body: $('#body').val()
        },
        success: function(json){
            $('#name').val('');
            $('#email').val('');
            $('#body').val('');
            console.log(json);
            $('.comments').append('<div id="comment-'+ json.pk +'" class="comment"><p class="info">New comment by ' + json.name + ' ' + json.created + '</p>' + json.body + '<a class="delete-comment" id="delete-post-'+ json.pk +'" href="">Delete</a></div>');
            console.log('success');
        },
        error: function(xhr){
            $(console.log(xhr.status + ': ' + xhr.responseText))
        }
    })
}

function delete_comment(pk) {
    if (confirm('Sure?') === true) {
        $.ajax({
            url: '.',
            type: 'DELETE',
            data: {
                pk: pk
            },
            success: function (json) {
                $('#comment-' + pk).hide();
                console.log('post deleted');
            },
            error: function(xhr) {
            $(console.log(xhr.status + ': ' + xhr.responseText))
            }
        })
    }
}


$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
