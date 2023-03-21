function change_state(obj) {
    if (obj.checked){
        //if checkbox is being checked, add a "checked" class
        obj.parentNode.classList.add("checked");
    }
    else{
        //else remove it
        obj.parentNode.classList.remove("checked");
    }
}


function make_graph() {

    // Determine TYPE of graph

    // Get state of surface temperature button
    const surfaceTemperature = document.getElementById('sfcTemp').checked;
    console.log(surfaceTemperature)

    // Get state of precipitation rate button
    const precipitationRate = document.getElementById('pcpRate').checked;
    console.log(precipitationRate)

    // Determine which MONTHS to include
    const jan = document.getElementById('jan').checked;
    const feb = document.getElementById('feb').checked;
    const mar = document.getElementById('mar').checked;
    const apr = document.getElementById('apr').checked;
    const may = document.getElementById('may').checked;
    const jun = document.getElementById('jun').checked;
    const jul = document.getElementById('jul').checked;
    const aug = document.getElementById('aug').checked;
    const sep = document.getElementById('sep').checked;
    const oct = document.getElementById('oct').checked;
    const nov = document.getElementById('nov').checked;
    const dec = document.getElementById('dec').checked;

    const months = []
    if (jan) { months.push("01") }
    if (feb) { months.push("02") }
    if (mar) { months.push("03") }
    if (apr) { months.push("04") }
    if (may) { months.push("05") }
    if (jun) { months.push("06") }
    if (jul) { months.push("07") }
    if (aug) { months.push("08") }
    if (sep) { months.push("09") }
    if (oct) { months.push("10") }
    if (nov) { months.push("11") }
    if (dec) { months.push("12") }


    console.log(months)

    const request = { "months": months, "plot": surfaceTemperature ? "sfc" : "pcp" }
    const requestJson = JSON.stringify(request);
    console.log(request)
    console.log(requestJson)
    $.ajax({
        url: "/",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(requestJson)
    });
}