//only works for Linux browsers since that is all we need
function mf_guess_client_arch(default_arch)
{
  arch = [default_arch];

  re = /Linux ([\d\w]+);/;
  match = re.exec(navigator.userAgent);
  arch = match[1];

  // return a list of possible matches for i386 and x86_64
  if (arch == 'i686') {
    arch = ['i686', 'i586', 'i486', 'i386'];
  } else if (arch == 'i586') {
    arch = ['i586', 'i486', 'i386'];
  } else if (arch == 'i486') {
    arch = ['i486', 'i386'];
  } else if (arch == 'x86_64') {
    arch = ['x86_64', 'i686', 'i586', 'i486', 'i386'];
  } else {
    arch = [arch];
  }

  return arch;
}
