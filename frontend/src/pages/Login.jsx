import { useMemo, useState } from "react";
import {
  ArrowLeft,
  ArrowRight,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  ShieldCheck,
  UserRound,
  BriefcaseBusiness,
  UsersRound,
  Sparkles,
} from "lucide-react";
import "./Login.css";

const roleDetails = {
  employee: {
    label: "Employee",
    icon: UserRound,
    accent: "blue",
    idLabel: "Employee ID",
    placeholder: "EMP001",
  },
  manager: {
    label: "Manager",
    icon: BriefcaseBusiness,
    accent: "purple",
    idLabel: "Manager ID",
    placeholder: "MANAGER001",
  },
  hr: {
    label: "HR",
    icon: UsersRound,
    accent: "green",
    idLabel: "HR ID",
    placeholder: "HR001",
  },
};

function Login() {
  const params = new URLSearchParams(window.location.search);
  const requestedRole = params.get("role");

  const roleKey = roleDetails[requestedRole] ? requestedRole : "employee";
  const role = useMemo(() => roleDetails[roleKey], [roleKey]);
  const RoleIcon = role.icon;

  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const goBack = () => {
    window.location.href = "/";
  };

  const login = async (event) => {
    event.preventDefault();

    if (!identifier.trim() || !password) {
      setError(`Please enter your ${role.idLabel.toLowerCase()} and password.`);
      return;
    }

    setLoading(true);
    setError("");

    try {
      /*
       * Authentication endpoint will be connected here.
       * For now the page validates the form and keeps the selected role.
       *
       * Expected future request:
       * POST /auth/login
       * {
       *   identifier,
       *   password,
       *   role: roleKey
       * }
       */

      const response = await fetch("http://127.0.0.1:8000/auth/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          identifier: identifier.trim(),
          password,
          role: roleKey,
        }),
      });

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(data.detail || data.message || "Invalid credentials.");
      }

      if (data.token) {
        localStorage.setItem("auth_token", data.token);
      }

      localStorage.setItem("user_role", roleKey);
      localStorage.setItem("user_identifier", identifier.trim());

      if (rememberMe) {
        localStorage.setItem("remember_me", "true");
      } else {
        localStorage.removeItem("remember_me");
      }

      if (roleKey === "manager") {
        window.location.href = "/manager";
      } else if (roleKey === "hr") {
        window.location.href = "/hr";
      } else {
        window.location.href = "/employee";
      }
    } catch (err) {
      console.error(err);
      setError(
        err.message ||
          "Unable to sign in. Please check the server and your credentials."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login-page">
      <div className="login-background login-bg-one" />
      <div className="login-background login-bg-two" />

      <section className="login-container">
        <button className="login-back" onClick={goBack} type="button">
          <ArrowLeft size={15} />
          Change role
        </button>

        <div className="login-brand">
          <div className="login-brand-icon">
            <Sparkles size={18} />
          </div>
          <div>
            <strong>AI Loss Prevention</strong>
            <span>Intelligent Knowledge System</span>
          </div>
        </div>

        <div className={`login-role-badge ${role.accent}`}>
          <RoleIcon size={16} />
          <span>{role.label} Login</span>
        </div>

        <div className="login-header">
          <h1>Welcome back</h1>
          <p>
            Sign in to access your {role.label.toLowerCase()} workspace.
          </p>
        </div>

        <form className="login-card" onSubmit={login}>
          <div className="login-card-role">
            <div className={`login-role-icon ${role.accent}`}>
              <RoleIcon size={21} />
            </div>

            <div>
              <span>Signing in as</span>
              <strong>{role.label}</strong>
            </div>

            <button type="button" onClick={goBack}>
              Change
            </button>
          </div>

          <div className="login-divider" />

          <label className="login-field">
            <span>{role.idLabel}</span>
            <div className="login-input-wrap">
              <UserRound size={17} />
              <input
                value={identifier}
                onChange={(event) => setIdentifier(event.target.value)}
                placeholder={role.placeholder}
                autoComplete="username"
              />
            </div>
          </label>

          <label className="login-field">
            <span>Password</span>
            <div className="login-input-wrap">
              <LockKeyhole size={17} />
              <input
                value={password}
                onChange={(event) => setPassword(event.target.value)}
                type={showPassword ? "text" : "password"}
                placeholder="Enter your password"
                autoComplete="current-password"
              />

              <button
                type="button"
                className="login-eye"
                onClick={() => setShowPassword((value) => !value)}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>
          </label>

          <div className="login-options">
            <label className="login-check">
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(event) => setRememberMe(event.target.checked)}
              />
              <span>Remember me</span>
            </label>

            <button type="button" className="login-forgot">
              Forgot password?
            </button>
          </div>

          {error && <div className="login-error">{error}</div>}

          <button
            className={`login-submit ${role.accent}`}
            type="submit"
            disabled={loading}
          >
            {loading ? "Signing in..." : "Sign In"}
            {!loading && <ArrowRight size={17} />}
          </button>

          <div className="login-security">
            <ShieldCheck size={14} />
            <span>Protected by role-based access control</span>
          </div>
        </form>

        <div className="login-support">
          <Mail size={14} />
          <span>Need access? Contact your administrator.</span>
        </div>

        <footer className="login-footer">
          <span>© 2026 AI Loss Prevention System</span>
          <span>Secure • Private • Intelligent</span>
        </footer>
      </section>
    </main>
  );
}

export default Login;