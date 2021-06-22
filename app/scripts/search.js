$(document).ready(function () {
    $("#listSearch").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#listProf a").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});