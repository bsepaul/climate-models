$(document).ready(function () {
    $('input[name="graphType"]').click(function () {
        var graph = $(this).attr("value");
        var target = $("." + graph);
        $(".options").not(target).hide();
        $(target).show();
    });
});