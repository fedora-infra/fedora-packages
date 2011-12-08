<script type="text/javascript">
function on_change(self) {
	$('#specfile').load('/_w/package.sources.spec #specfile', {
		'package_name': '${w.package_name}',
		'branch': self.value
		});
}
</script>

${w.children[0].display(on_change='on_change')}

<br/>

<div id="specfile">
${w.text}
</div>
