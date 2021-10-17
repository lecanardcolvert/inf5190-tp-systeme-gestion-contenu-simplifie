$(document).ready(function() {
    $("#article-new-form").submit(function(event) {
        var form = $(this);
        var url = form.attr("action");

        event.preventDefault();
        $("#article-new-submit").prop('disabled', true);
        validateForm(url, 'post', form.serialize());
        $("#article-new-submit").prop('disabled', false);
    });

    $("#article-edit-form").submit(function(event) {
        var form = $(this);
        var url = form.attr("action");

        event.preventDefault();
        $("#article-edit-submit").prop('disabled', true);
        validateForm(url, 'post', form.serialize());
        $("#article-edit-submit").prop('disabled', false);
    });
});

async function validateForm(url, type, data) {
    let result;

    try {
        result = await $.ajax({
            url: url,
            type: type,
            data: data,
            dataType: "json",
            success: function(res) {
                if (res.redirect) {
                    window.location.href = res.redirect;
                } else {
                    for (const key in res.err) {
                        $("#" + key).removeClass("is-valid");
                        $("#" + key).addClass("is-invalid");
                        $("#" + key + "-help").removeClass("valid-feedback");
                        $("#" + key + "-help").addClass("invalid-feedback");
                        $("#" + key + "-help").text(res.err[key]);
                    }
                    for (const key in res.ok) {
                        $("#" + key).removeClass("is-invalid");
                        $("#" + key).addClass("is-valid");
                        $("#" + key + "-help").removeClass("invalid-feedback");
                        $("#" + key + "-help").addClass("valid-feedback");
                        $("#" + key + "-help").text(res.ok[key]);
                    }
                }
            },
            error: function(xhr, status, error){
                var errorMessage = xhr.status + ': ' + xhr.statusText
                alert('Erreur : ' + errorMessage);
            }
        });

        return result;
    } catch (error) {
        console.error(error);
    }
}