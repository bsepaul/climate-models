function change_state(obj) {
    if (obj.checked) {
        //if checkbox is being checked, add a "checked" class
        obj.parentNode.classList.add("checked");
    }
    else {
        //else remove it
        obj.parentNode.classList.remove("checked");
    }
}


// function make_graph() {

//     // Determine TYPE of graph

//     // Get state of surface temperature button
//     const surfaceTemperatureChecked = document.getElementById('sfcTemp').checked;

//     // Get state of precipitation rate button
//     const precipitationRateChecked = document.getElementById('pcpRate').checked;

//     // Get state of precipitation amount button
//     const precipitationAmountChecked = document.getElementById('pcpAmnt').checked;

//     // Add plot types to a list of plots
//     const plots = [];
//     if (surfaceTemperatureChecked) { plots.push("sfcTemp") };
//     if (precipitationRateChecked) { plots.push("pcpRate") };
//     if (precipitationAmountChecked) { plots.push("pcpAmnt") };

//     // Determine which MONTHS to include
//     const jan = document.getElementById('jan').checked;
//     const feb = document.getElementById('feb').checked;
//     const mar = document.getElementById('mar').checked;
//     const apr = document.getElementById('apr').checked;
//     const may = document.getElementById('may').checked;
//     const jun = document.getElementById('jun').checked;
//     const jul = document.getElementById('jul').checked;
//     const aug = document.getElementById('aug').checked;
//     const sep = document.getElementById('sep').checked;
//     const oct = document.getElementById('oct').checked;
//     const nov = document.getElementById('nov').checked;
//     const dec = document.getElementById('dec').checked;

//     // Add month numbers to a list of months
//     const months = []
//     if (jan) { months.push("01") }
//     if (feb) { months.push("02") }
//     if (mar) { months.push("03") }
//     if (apr) { months.push("04") }
//     if (may) { months.push("05") }
//     if (jun) { months.push("06") }
//     if (jul) { months.push("07") }
//     if (aug) { months.push("08") }
//     if (sep) { months.push("09") }
//     if (oct) { months.push("10") }
//     if (nov) { months.push("11") }
//     if (dec) { months.push("12") }

//     // Configure data to send in the request (list of months and list of plot types to include)
//     // Example: A plot of the average surface temperature for the months January, February, and March
//     // request = { "months": ["01", "02", "03"], "plot": ["sfcTemp"]}
//     const request = { "months": months, "plot": plots }
//     const requestJson = JSON.stringify(request);

//     // POST the request to be caught
//     $.ajax({
//         url: "/",
//         type: "POST",
//         contentType: "application/json",
//         data: JSON.stringify(requestJson)
//     });
// }