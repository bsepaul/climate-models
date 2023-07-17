$(document).ready(function () {

    // By default, single time is selected so on load hide compare time selection and make sure single time selection is shown
    $(".compare-time").hide();
    $(".diff-type").hide();
    $(".single-time").show();

    // If user selects either compare-time or single-time, show the correct timeline selections based on selection
    $('input[name="graphType"]').click(function () {
        var type = $(this).attr("value");
        if (type == 'compare') {
            $(".single-time").hide();
            $(".compare-time").show();
            $(".diff-type").show();
        } else {
            $(".compare-time").hide();
            $(".single-time").show();
            $(".diff-type").hide();
        }
    })

    // For compare time selection, make sure only two time selections are selected at one time
    $('input[name="compareTimePeriod"]').click(function () {
        var reached_max = $("input:checkbox:checked").length >= 2;
        $('input[name="compareTimePeriod"]').not(":checked").attr("disabled", reached_max);
    })

    // Show the graph variables for the selected graph variable (color map choices, elevation slider, etc.)
    $('input[name="graphVariable"]').click(function () {
        var graph = $(this).attr("value");
        var target = $("." + graph);
        $(".options").not(target).hide();
        $(target).show();
    });
});