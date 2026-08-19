import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import LandingPage from "./pages/LandingPage";
import RoleSelection from "./pages/RoleSelection";
import Login from "./pages/Login";

import EmployeeDashboard from "./pages/EmployeeDashboard";
import ManagerDashboard from "./pages/ManagerDashboard";
import HRDashboard from "./pages/HRDashboard";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* ================= PUBLIC ROUTES ================= */}

        <Route
          path="/"
          element={<LandingPage />}
        />

        <Route
          path="/roles"
          element={<RoleSelection />}
        />

        <Route
          path="/login"
          element={<Login />}
        />


        {/* ================= EMPLOYEE ================= */}

        <Route
          path="/employee"
          element={
            <ProtectedRoute allowedRole="employee">
              <EmployeeDashboard />
            </ProtectedRoute>
          }
        />


        {/* ================= MANAGER ================= */}

        <Route
          path="/manager"
          element={
            <ProtectedRoute allowedRole="manager">
              <ManagerDashboard />
            </ProtectedRoute>
          }
        />


        {/* ================= HR ================= */}

        <Route
          path="/hr"
          element={
            <ProtectedRoute allowedRole="hr">
              <HRDashboard />
            </ProtectedRoute>
          }
        />


        {/* ================= UNKNOWN ROUTE ================= */}

        <Route
          path="*"
          element={<Navigate to="/" replace />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;