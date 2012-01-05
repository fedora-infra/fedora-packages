<html>
<head></head>
<body>
% for child in w.children:
	${child.display(package=w.package)}
% endfor
</body>
</html>
