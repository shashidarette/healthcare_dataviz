// This is the java-script file with client logic specific for Focus Group
var focusGroup = [];

// on document ready : initalize the UI elements
$(document).ready(function () {
    loadGPProfiles();
    updateDrugGroups();
    focusGroup = getQueryOrgs();
    getOrgCosts(focusGroup);
})