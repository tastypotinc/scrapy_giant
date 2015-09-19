
function plotTableData(result){
    var stockitem = result.stockitem;
    var credititem = result.credititem;
    var futureitem = result.futureitem;
    var data = [];

    // try iter to fill all fields
    $.each(stockitem[0].datalist, function(d_idx, d_it) {
        var date = new Date(d_it.date);
        data.push({
            "date": yyyymmdd(date),
            "open": parseFloat(d_it.open.toFixed(2)),
            "close": parseFloat(d_it.close.toFixed(2)),
            "high": parseFloat(d_it.high.toFixed(2)),
            "low": parseFloat(d_it.low.toFixed(2)),
            "volume": parseInt(d_it.volume.toFixed()),
            "finaused" : 0.00,
            "bearused": 0.00,
            "fopen": 0.00,
            "fclose": 0.00,
            "fvolume": 0,
            "event": ""
        });
    });

    var ndata = $.extend(true, [], data);
    $.each(credititem[0].datalist, function(d_idx, d_it) {
        var date = new Date(d_it.date);
        var rst = $.grep(ndata, function(e){ return e.date == yyyymmdd(date); });
        if (rst.length != 0) {
            rst[0].finaused = parseFloat(d_it.financeused.toFixed(2));
            rst[0].bearused = parseFloat(d_it.bearishused.toFixed(2));
        }
    });

    var fdata = $.extend(true, [], ndata);
    $.each(futureitem[0].datalist, function(d_idx, d_it) {
        var date = new Date(d_it.date);
        var rst = $.grep(fdata, function(e){ return e.date == yyyymmdd(date); });
        if (rst.length != 0) {
            rst[0].fopen = parseFloat(d_it.fopen.toFixed(2));
            rst[0].fclose = parseFloat(d_it.fclose.toFixed(2));
            rst[0].fvolume = parseInt(d_it.fvolume.toFixed());
        }
    });

    $('#stockdetail_table').dynatable({
        dataset: {
            records: fdata
        }
    });

    //console.log(data);
}