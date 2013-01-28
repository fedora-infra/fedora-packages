<div class="grid_filter">
  <label for="release_id"><h4>Release:</h4></label>
</div>
<select name="release_id" id="release_select" onChange="${w.on_change}(this)">
 % for i, release in enumerate(w.releases_table):
   <% selected = i == 0 and 'selected="selected"' or '' %>
   <option ${selected} value="${str(release['value'])}">${release['label']}</option>
 % endfor
</select>
