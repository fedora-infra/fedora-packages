<% import tg %>
<div
     id="${id}"
     class="login panel">

    <h3>Log In</h3>
    <form action="${tg.url('/login_handler')}" method="POST">
        <input type="hidden" name="came_from" value="${came_from}"></input>
        <div>
            <span>
                User Name
            </span>
            <input type="text" name="login"></input>
        </div>
        <div>
            <span>
                Password
            </span>
            <input type="password" name="password"></input>
        </div>
        <input class="button" type="submit" value="Login"/>
        <br />
        <a href="https://admin.fedoraproject.org/accounts/user/new" target="_blank" class="small-text">Need an account?</a><br />
        <a href="https://admin.fedoraproject.org/accounts/user/resetpass" target="_blank" class="small-text">Forget your password?</a>
    </form>
</div>