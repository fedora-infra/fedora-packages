<%namespace file="diffstat.mak" import="render_diffstat"/>

% if w.diffstat:
<b>Summary of changes in this patch:</b>
${render_diffstat(w.diffstat)}
% endif
<br/>
${w.text}
