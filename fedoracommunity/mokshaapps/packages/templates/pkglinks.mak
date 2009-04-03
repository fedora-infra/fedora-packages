<div id="${id}" class="infra-toolbar">
    <p>View this package in other Fedora Infrastructure systems:</p>
    <ul>
      <li><a href="https://admin.fedoraproject.org/updates/${package}"
             target="_blank">
             <img border=0 src="/images/16_bodhi.png" />
             <span>Updates</span>
          </a>
      </li>
      <li><a href="http://koji.fedoraproject.org/koji/search?terms=${package}&type=package&match=exact" target="_blank" >
              <img border=0 src="/images/16_koji.png" />
              <span>Builds</span>
          </a>
      </li>
      <li><a href="https://admin.fedoraproject.org/pkgdb/bugs/name/${package}" target="_blank" >
              <img border=0 src="/images/16_bugs.png" />
              <span>Bugs</span>
          </a>
      </li>
      <li><a href="http://cvs.fedoraproject.org/viewvc/rpms/${package}" target="_blank" >
              <img border=0 src="/images/16_sources.png" />
              <span>Source</span>
          </a>
      </li>
      <li><a href="https://admin.fedoraproject.org/pkgdb/packages/name/${package}" target="_blank" >
              <img border=0 src="/images/16_pkgdb.png" />
              <span>Package Info</span>
          </a>
      </li>
    </ul>
</div>
