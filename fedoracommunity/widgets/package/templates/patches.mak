<table>
% for patch in sorted(w.patches):
    <tr id="${patch}">
        <td><a href="#" onclick="return show_patch('${patch}');">${patch}</a></td>
        <td>Added ${w.patches[patch][0]} ago</td>
        <td>(${w.patches[patch][1]})</td>
    </tr>
% endfor
</table>

<script type="text/javascript">
function show_patch(patch) {
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
</script>
