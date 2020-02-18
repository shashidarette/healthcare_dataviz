// referred tutorial from plot.ly/python/3d-scatter-plots/
var x = [];
var y = [];
var z = [];
var text = [];
var name = [];
var diabeticPCount = [];
var avgAge = [];
var clusterIndex = [];
var actCost = [];
var focusGroup = [];

// data params
var params =
    {
        'ITEMS': 'ITEMS',
        'NIC': 'Net Ingridient Cost',
        'ACT COST': 'Actual Cost',
        'QUANTITY': 'QUANTITY',
        'TotalSize': 'TotalSize',
        'AvgAgeProfile': 'AvgAgeProfile',
        'PerPatient_NIC': 'PerPatient_NIC',
        'PerPatient_ActCost': 'PerPatient_ActCost',
        '% aged 65+ years': '% aged 65+ years',
        'Number of Diabetic Patients': 'Number of Diabetic Patients', // 'Diabetes: QOF prevalence (17+)'
        '% of Diabetes patients': '% of Diabetes patients',
        'Number of Hypertension Patients': 'Number of Hypertension Patients', // 'Hypertension: QOF prevalence (all ages)'
        '% of Hypertension patients': '% of Hypertension patients',
        'IMD': 'IMD - Index of Multiple of Deprivation'
    };

// drug groups
var drugGroups =
    {
        //'Total Costs': { fileName: 'ClusterDiabetes.csv' },
        'Metformin': { fileName: 'CostsByMetforminByCluster.csv' },
        'Oral hypoglycaemics': { fileName: 'CostsByOralByCluster.csv' },
        'Gliptins': { fileName: 'CostsByGliptinsByCluster.csv' },
        'Insulin': { fileName: 'CostsByInsulinByCluster.csv' },
        'Insulin2': { fileName: 'CostsByInsulinByCluster.csv' },
        'Viagra and others': { fileName: 'CostsByViagraByCluster.csv' },
    };

//SUB_CHAPTER,ITEMS,NIC,ACT COST,QUANTITY
var paramsData = [];
var maxTotalSize = 4;
var minSize = 4;

var drugGroupCosts = [];
var areaName = [];
var areaCode = [];
var practiceName = [];
var practiseCode = [];

// load the costs merged data and updated the associated arrays
Plotly.d3.csv('./CostsDataMerged.csv', function (err, rows) {
    function unpack(rows, key) {
        return rows.map(function (row) {
            return row[key];
        });
    }

    paramsData['IMD'] =  unpack(rows, 'Deprivation score (IMD 2015)');
    paramsData['AvgAgeProfile'] = unpack(rows, 'AvgAgeProfile');
    paramsData['ITEMS'] = unpack(rows, 'ITEMS  ');
    paramsData['ACT COST'] = unpack(rows, 'ACT COST   ');
    paramsData['QUANTITY'] = unpack(rows, 'QUANTITY');
    paramsData['NIC'] = unpack(rows, 'NIC        ');

    paramsData['TotalSize'] = unpack(rows, 'TotalSize');
    paramsData['PerPatient_NIC'] = unpack(rows, 'PerPatient_NIC');
    paramsData['PerPatient_ActCost'] = unpack(rows, 'PerPatient_ActCost');
    paramsData['% aged 65+ years'] = unpack(rows, '% aged 65+ years');
    paramsData['% of Diabetes patients'] = unpack(rows, '% of Diabetes patients');
    paramsData['Number of Diabetic Patients'] = unpack(rows, 'Diabetes: QOF prevalence (17+)');
    paramsData['Number of Hypertension Patients'] = unpack(rows, 'Hypertension: QOF prevalence (all ages)');
    practiceName = unpack(rows, 'Practice Name');
    practiseCode = unpack(rows, 'PRACTICE');
    areaCode = unpack(rows, 'Area Team Code');
    areaName = unpack(rows, 'PCO Name');
    clusterIndex = unpack(rows, 'ClusterNumber');

    // PRACTICE,SUB_CHAPTER,ITEMS,NIC,ACT COST,QUANTITY,ClusterNumber
    drugGroupCosts['Metformin'] = [];
    drugGroupCosts['Metformin']['SUB_CHAPTER'] = unpack(rows, 'Metformin_SUB_CHAPTER');
    drugGroupCosts['Metformin']['ITEMS'] = unpack(rows, 'Metformin_ITEMS');
    drugGroupCosts['Metformin']['NIC'] = unpack(rows, 'Metformin_NIC');
    drugGroupCosts['Metformin']['ACT COST'] = unpack(rows, 'Metformin_ACT COST');
    drugGroupCosts['Metformin']['QUANTITY'] = unpack(rows, 'Metformin_QUANTITY');
    
    // PRACTICE,SUB_CHAPTER,ITEMS,NIC,ACT COST,QUANTITY,ClusterNumber
    drugGroupCosts['Viagra and others'] = [];
    drugGroupCosts['Viagra and others']['SUB_CHAPTER'] = unpack(rows, 'ViagraOthers_SUB_CHAPTER');
    drugGroupCosts['Viagra and others']['ITEMS'] = unpack(rows, 'ViagraOthers_ITEMS');
    drugGroupCosts['Viagra and others']['NIC'] = unpack(rows, 'ViagraOthers_NIC');
    drugGroupCosts['Viagra and others']['ACT COST'] = unpack(rows, 'ViagraOthers_ACT COST');
    drugGroupCosts['Viagra and others']['QUANTITY'] = unpack(rows, 'ViagraOthers_QUANTITY');

    drugGroupCosts['Gliptins'] = [];
    drugGroupCosts['Gliptins']['SUB_CHAPTER'] = unpack(rows, 'Gliptins_SUB_CHAPTER');
    drugGroupCosts['Gliptins']['ITEMS'] = unpack(rows, 'Gliptins_ITEMS');
    drugGroupCosts['Gliptins']['NIC'] = unpack(rows, 'Gliptins_NIC');
    drugGroupCosts['Gliptins']['ACT COST'] = unpack(rows, 'Gliptins_ACT COST');
    drugGroupCosts['Gliptins']['QUANTITY'] = unpack(rows, 'Gliptins_QUANTITY');

    drugGroupCosts['Insulin1'] = [];
    drugGroupCosts['Insulin1']['SUB_CHAPTER'] = unpack(rows, 'Insulin1_SUB_CHAPTER');
    drugGroupCosts['Insulin1']['ITEMS'] = unpack(rows, 'Insulin1_ITEMS');
    drugGroupCosts['Insulin1']['NIC'] = unpack(rows, 'Insulin1_NIC');
    drugGroupCosts['Insulin1']['ACT COST'] = unpack(rows, 'Insulin1_ACT COST');
    drugGroupCosts['Insulin1']['QUANTITY'] = unpack(rows, 'Insulin1_QUANTITY');

    drugGroupCosts['Insulin2'] = [];
    drugGroupCosts['Insulin2']['SUB_CHAPTER'] = unpack(rows, 'Insulin2_SUB_CHAPTER');
    drugGroupCosts['Insulin2']['ITEMS'] = unpack(rows, 'Insulin2_ITEMS');
    drugGroupCosts['Insulin2']['NIC'] = unpack(rows, 'Insulin2_NIC');
    drugGroupCosts['Insulin2']['ACT COST'] = unpack(rows, 'Insulin2_ACT COST');
    drugGroupCosts['Insulin2']['QUANTITY'] = unpack(rows, 'Insulin2_QUANTITY');

    drugGroupCosts['Oral hypoglycaemics'] = [];
    drugGroupCosts['Oral hypoglycaemics']['SUB_CHAPTER'] = unpack(rows, 'OralHypo_SUB_CHAPTER');
    drugGroupCosts['Oral hypoglycaemics']['ITEMS'] = unpack(rows, 'OralHypo_ITEMS');
    drugGroupCosts['Oral hypoglycaemics']['NIC'] = unpack(rows, 'OralHypo_NIC');
    drugGroupCosts['Oral hypoglycaemics']['ACT COST'] = unpack(rows, 'OralHypo_ACT COST');
    drugGroupCosts['Oral hypoglycaemics']['QUANTITY'] = unpack(rows, 'OralHypo_QUANTITY');

    maxTotalSize = Math.max(...paramsData['TotalSize']);

    var hoverInfo = document.getElementById('hoverinfo');

    var clusterData = {
        x: paramsData['IMD'],
        y: paramsData['AvgAgeProfile'],
        z: paramsData['% of Diabetes patients'],
        text: practiseCode,
        hovermode: 'closest',
        hoverinfo: 'text',
        mode: 'markers',
        line: {
            color: 'rgba(255, 0, 0, 1)',
        },
        marker: {
            size: 8,
            line: {
                color: 'rgba(0, 0, 0, 0)',
                width: 0
            },
            //color: clusterIndex,
            opacity: 1,
            colorscale: 'Bluered' // Greys, YlGnBu, Greens, YlOrRd, Bluered, RdBu, Reds, Blues, Picnic, Rainbow, Portland, Jet, Hot, Blackbody, Earth, Electric, Viridis, Cividis
        },
        // start with all points
        transforms: [
        {
            type: 'filter',
            target: clusterIndex,
            operation: '>',
            value: '-1',
        }, {
            type: 'groupby',
            groups: clusterIndex,
            // filter at cluster level
            styles: [
              { target: 0, value: { marker: { text: 'Cluster 0' } } }, // , color: 'red'
              { target: 1, value: { marker: { text: 'Cluster 1' } } }, // , color: 'blue'
              { target: 2, value: { marker: { text: 'Cluster 2' } } }, // , color: 'orange'
              { target: 3, value: { marker: { text: 'Cluster 3' } } }, // , color: 'green'
            ]
        }],
        type: 'scatter3d'
    };
    var data = [clusterData];
    var layout = {
        title: 'Cluster Analysis of General Practices in UK',
        dragmode: true,
        hovermode: 'closest',
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 50,
            pad: 100,
            autoexpand : true
        },
        scene: {
            // default is cube: aspectmode: 'data',
            xaxis: {
                title: 'IMD (Index of Multiple Deprivation)',
                titlefont: {
                    color: 'blue'
                }
            },
            yaxis: {
                title: 'AvgAgeProfile',
                titlefont: {
                    color: 'blue'
                }
            },
            zaxis: {
                title: '% of Diabetes patients',
                titlefont: {
                    color: 'blue'
                }
            }
        }
    };
    var clusterPlot = document.getElementById('3DClusterVizDiv');

    Plotly.newPlot('3DClusterVizDiv', data, layout);

    clusterPlot.on('plotly_hover', function (eventData) {
        var pcode = eventData.points[0].text;
        var index = practiseCode.findIndex(c => c == pcode);
        updateHoverInfo(index);
    })
    .on('plotly_unhover', function (eventData) {
    })
    .on('plotly_click', function(eventData) {
    })
    .on('plotly_restyle', function(eventData) {
    })
    .on('plotly_relayout', function (eventData) {
    });

    update2DPlot('ACT COST', '% of Diabetes patients', 'Total Costs');
});

// update hover info
function updateHoverInfo(index) {
    $('#practice_code').text(practiseCode[index]);
    $('#name').text(practiceName[index]);
    $('#areacode').text(areaCode[index] + ' ' + areaName[index]);
    $('#avgage').text(paramsData['AvgAgeProfile'][index]);
    $('#avg65age').text(paramsData['% aged 65+ years'][index]);
    $('#pcount').text(paramsData['Number of Diabetic Patients'][index]);
    $('#imd').text(paramsData['IMD'][index]);
    $('#totalSize').text(paramsData['TotalSize'][index]);
    $('#hypPCount').text(paramsData['Number of Hypertension Patients'][index]);
}

// update costs info
function updateCostInfo(index) {
    $('#drug_group_name').text(drugGroupSelected);
    var items = 'NA';
    var quantity = 'NA';
    var nic = 'NA';
    var act_cost = 'NA';

    if (drugGroupSelected == 'Total Costs' || drugGroupSelected == 'NA' || drugGroupSelected == "") {
        act_cost = paramsData['ACT COST'][index];
        nic = paramsData['NIC'][index];
        items = paramsData['ITEMS'][index];
        quantity = paramsData['QUANTITY'][index];
    } else {
        act_cost = drugGroupCosts[drugGroupSelected]['ACT COST'][index];
        nic = drugGroupCosts[drugGroupSelected]['NIC'][index];
        items = drugGroupCosts[drugGroupSelected]['ITEMS'][index];
        quantity = drugGroupCosts[drugGroupSelected]['QUANTITY'][index];
    }

    $('#items').text(items);
    $('#quanity').text(quantity);
    $('#nic').text(nic);
    $('#act_cost').text(act_cost);
}

// update 2D plot
var drugGroupSelected = "NA";
function update2DPlot(x, y, drugGroup) {
    var xData = [];
    var yData = [];

    // drug groups only have ITEMS,NIC,ACT COST,QUANTITY
    var considerx = false;
    var considery = false;
    if (drugGroup != undefined && drugGroup != 'Total Costs' && drugGroup != "") {
        drugGroupSelected = drugGroup;
        if (x.includes('ITEMS') || x.includes('NIC') || x.includes('ACT COST') || x.includes('QUANTITY')) {
            considerx = true;
        }
        if (y.includes('ITEMS') || y.includes('NIC') || y.includes('ACT COST') || y.includes('QUANTITY')) {
            considery = true;
        }
        if (considerx) {
            xData = drugGroupCosts[drugGroup][x];
        }
        if (considery) {
            yData = drugGroupCosts[drugGroup][y];
        }
    }
    if (!considerx) {
        xData = paramsData[x];
    }
    if (!considery) {
        yData = paramsData[y];
    }

    if (xData != undefined && yData != undefined) {
        var maxX = Math.max(...xData);
        maxY *= 1.1;

        var maxY = Math.max(...yData);
        maxY *= 1.1;

        var TwoDlayout = {
            xaxis: {
                title: x,
                titlefont: {
                    color: 'grey'
                },
                range: [0, maxX]
            },
            yaxis: {
                title: y,
                titlefont: {
                    color: 'grey'
                },
                range: [0, maxY]
            },
            hovermode: 'closest',
            title: '2D Plot - Cluster Analysis of General Practices in UK',
        };

        var maxTotalSize = Math.max(...paramsData['TotalSize']);
        var TwoDClusterData = {
            x: xData,
            y: yData,
            text: practiseCode,
            hoverinfo: 'text',
            mode: 'markers',
            line: {
                color: 'rgba(255, 0, 0, 1)',
            },
            marker: {
                size: paramsData['TotalSize'],
                sizeref: 2. * maxTotalSize / (50. ^ 2),
                sizemin: minSize,
                line: {
                    color: 'rgba(0, 0, 0, 0)',
                    width: 0
                },
                //color: clusterIndex,
                opacity: 1,
                colorscale: 'Cividis' // Greys, YlGnBu, Greens, YlOrRd, Bluered, RdBu, Reds, Blues, Picnic, Rainbow, Portland, Jet, Hot, Blackbody, Earth, Electric, Viridis, Cividis
            },
            type: 'scatter',
            // start with all points
            transforms: [
            {
                type: 'filter',
                target: clusterIndex,
                operation: '>',
                value: '-1'
            }, {
                type: 'groupby',
                groups: clusterIndex,
                // filter at cluster level
                styles: [
                  { target: '0', value: { marker: { text: 'Cluster 0' } } },
                  { target: '1', value: { marker: { text: 'Cluster 1' } } },
                  { target: '2', value: { marker: { text: 'Cluster 2' } } },
                  { target: '3', value: { marker: { text: 'Cluster 3' } } },
                ]
            }],
        };

        var Twodata = [TwoDClusterData];
        Plotly.newPlot('2DFilterdDiv', Twodata, TwoDlayout);
        var TwoDclusterPlot = document.getElementById('2DFilterdDiv');

        TwoDclusterPlot.on('plotly_hover', function (eventData) {
            var index = eventData.points[0].pointIndex;
            updateHoverInfo(index);
            updateCostInfo(index);
        });
    }
}

// update the plot related params
function updateParams() {    
    updateXParams();
    updateYParams();
    updateDrugGroups();
}

var optionElement = '<option>';
// update x-axis parameters
function updateXParams() {
    var xparams = $("#xaxis_cols");
    var firstOption = $(optionElement).text('Choose a parameter');
    firstOption.attr('value', "");
    xparams.append(firstOption);

    for (var p in params) {
        var option = $(optionElement).text(params[p]);
        option.attr('value', p);
        xparams.append(option);
    }
}

// update y-axis parameters
function updateYParams() {
    var yparams = $("#yaxis_cols");
    var firstOption = $(optionElement).text('Choose a parameter');
    firstOption.attr('value', "");
    yparams.append(firstOption);

    for (var p in params) {
        var option = $(optionElement).text(params[p]);
        option.attr('value', p);
        yparams.append(option);
    }
}

// update 2D plot based on selected x and y param
function btnUpdateParams(object) {
    var xparam = $("#xaxis_cols")["0"].value;
    var yparam = $("#yaxis_cols")["0"].value;
    var drugGroup = $("#drug_groups")["0"].value;
    if (xparam != undefined && xparam != "" &&
        yparam != undefined && yparam != "" &&
        drugGroup != undefined) {
        update2DPlot(xparam, yparam, drugGroup);
    }
}

// get practice code
function getPracticeCode() {
    return $('#practice_code').text();
}

// add practice to focus
function btnAddToFocus(object) {
    var practice = getPracticeCode();
    var id = '#' + practice;

    var element = $('#focus_group').children(id);
    if (element.length == 0) {
        var practiceButton = $('<button type="button" class="btn btn-primary" onclick="onFocusGroupClick(this)"></button>').text(practice);
        practiceButton.attr('id', practice);
        $('#focus_group').append(practiceButton);
        focusGroup.push(practice);
    }
}

// remove practice from focus
function btnRemoveFocus(object) {
    var practice = getPracticeCode();
    var id = '#' + practice;
    var element = $('#focus_group').children(id);
    if (element.length == 1) {
        element[0].remove();
        focusGroup.push(practice);
    }
}

function onFocusGroupClick(object) {

}

// on document ready
$(document).ready(function () {
    updateParams();
})