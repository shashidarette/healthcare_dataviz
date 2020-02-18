// This is the java-script file with client logic specific for Drug Groups

// pre-defined drug groups and BNF mapping
//Metformin
//OralHypo
//Gliptins
//Insulin1
//Insulin2
//ViagraOthers
var drugGroupMapping =
{
    'Metformin': 'Metformin_',
    'Oral hypoglycaemics': 'OralHypo_',
    'Gliptins': 'Gliptins_',
    'Insulin1': 'Insulin1_',
    'Insulin2': 'Insulin2_',
    'Viagra and others': 'ViagraOthers_',
};

var drugGroupBnfMapping =
{
    'Metformin': '0601022',
    'Oral hypoglycaemics': '0601021',
    'Gliptins': '0601023',
    'Insulin1': '0601011',
    'Insulin2': '0601012',
    'Viagra and others': '0704050',
};

var optionElement = '<option>';
// add drug groups in the UI elements
function addDrugGroups(objectId) {
    var dgParams = $(objectId);
    var firstOption = $('<option>').text('Choose a parameter');
    firstOption.attr('value', "");
    dgParams.append(firstOption);

    for (var p in drugGroupMapping) {
        var option = $(optionElement).text(p);
        option.attr('value', p);
        dgParams.append(option);
    }
}

// update drug groups
function updateDrugGroups() {
    addDrugGroups('#drug_groups');
    addDrugGroups('#fg_drug_groups');
}