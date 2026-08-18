import EmployeeDashboard from "./pages/EmployeeDashboard";
import ManagerDashboard from "./pages/ManagerDashboard";
import HRDashboard from "./pages/HRDashboard";
import RoleSelection from "./pages/RoleSelection";
import Login from "./pages/Login";
import LandingPage from "./pages/LandingPage";

function App() {
  const path = window.location.pathname;

  // Main landing page
  if (path === "/") {
    return <LandingPage />;
  }

  // Role selection
  if (path === "/roles") {
    return <RoleSelection />;
  }

  // Login
  if (path === "/login") {
    return <Login />;
  }

  // Dashboards
  if (path === "/manager") {
    return <ManagerDashboard />;
  }

  if (path === "/hr") {
    return <HRDashboard />;
  }

  if (path === "/employee") {
    return <EmployeeDashboard />;
  }

  return <LandingPage />;
}

export default App;