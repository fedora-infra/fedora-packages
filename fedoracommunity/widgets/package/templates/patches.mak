<center><a id="diffstat_link" href="#" onclick="return toggle_diffstat()">Show summary of all patches</a></center>
<div id="diffstat" style="display:none"><pre>${w.diffstat}</pre></div>
<br/>
<table>
% for patch in sorted(w.patches):
    <tr id="${patch}">
        <td><a href="#" onclick="return toggle_patch('${patch}');">${patch}</a></td>
        <td>Added ${w.patches[patch][0]} ago</td>
        <td>(${w.patches[patch][1]})</td>
    </tr>
% endfor
</table>

<script type="text/javascript">
function toggle_patch(patch) {
	var tr = $('#' + patch.replace(/\./g, '\\.'));

	/* If we're already showing the patch, hide it */
	if ( tr.next().attr('id') == 'patch' ) {
		tr.next().remove();
		return false;
	}

	tr.after(
	  $('<tr/>', {id: 'patch'}).append(
		  $('<td/>', {colspan: 3}).load('/widgets/package.sources.patch',
		  	  {package: '${w.package}', patch: patch})));
	return false;
}


function toggle_diffstat() {
	if ( $('#diffstat').is(":visible") ) {
		$('#diffstat').hide();
		$('#diffstat_link').text('Show summary of all patches');
	} else {
		$('#diffstat').show();
		$('#diffstat_link').text('Hide summary of all patches');
	}
}
</script>
