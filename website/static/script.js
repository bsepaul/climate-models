$(document).ready(function () {
    $('input[type="radio"]').click(function () {
        var graph = $(this).attr("value");
        var target = $("." + graph);
        console.log(graph)
        console.log(target)
        $(".options").not(target).hide();
        $(target).show();
    });
});