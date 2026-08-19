import { Navigate } from "react-router-dom";

function ProtectedRoute({ children, allowedRole }) {
  const token = localStorage.getItem("auth_token");
  const userRole = localStorage.getItem("user_role");

  // No JWT → go to login
  if (!token) {
    return <Navigate to="/login" replace />;
  }

  // Wrong role → go to correct dashboard
  if (allowedRole && userRole !== allowedRole) {
    if (userRole === "manager") {
      return <Navigate to="/manager" replace />;
    }

    if (userRole === "hr") {
      return <Navigate to="/hr" replace />;
    }

    return <Navigate to="/employee" replace />;
  }

  return children;
}

export default ProtectedRoute;