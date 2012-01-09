<html>
<head></head>
<body>
% for child in w.children:
	${child.display(package=w.main_package)}
% endfor
</body>
</html>
