<script type="text/javascript">

function done_cb(data) {
	$('#specfile').html(data['text']);
}

function on_change(self) {
	moksha.connector_load('git', 'get_spec', {
			'package': '${w.package_name}',
			'branch': self.value
			}, done_cb);
}

</script>

${w.children[0].display(package=w.package_name, on_change='on_change')}

<br/>

<div id="specfile">
${w.text}
</div>
