import { useState } from "react";
import {
  UserRound,
  BriefcaseBusiness,
  UsersRound,
  ArrowRight,
  ShieldCheck,
  Sparkles,
} from "lucide-react";
import "./RoleSelection.css";

const roles = [
  {
    id: "employee",
    title: "Employee",
    description: "Access your tasks, projects, knowledge and AI assistant.",
    icon: UserRound,
    accent: "blue",
  },
  {
    id: "manager",
    title: "Manager",
    description: "Manage your team, projects, tasks and team knowledge.",
    icon: BriefcaseBusiness,
    accent: "purple",
  },
  {
    id: "hr",
    title: "HR",
    description: "View organization-wide employees, projects and activity.",
    icon: UsersRound,
    accent: "green",
  },
];

function RoleSelection() {
  const [selectedRole, setSelectedRole] = useState("");

  const continueToLogin = () => {
    if (!selectedRole) return;

    window.location.href = `/login?role=${selectedRole}`;
  };

  return (
    <main className="role-page">
      <div className="role-background-shape role-shape-one" />
      <div className="role-background-shape role-shape-two" />

      <section className="role-container">
        <div className="role-brand">
          <div className="role-brand-icon">
            <Sparkles size={19} />
          </div>
          <div>
            <strong>AI Loss Prevention</strong>
            <span>Intelligent Knowledge System</span>
          </div>
        </div>

        <div className="role-header">
          <div className="role-header-badge">
            <ShieldCheck size={15} />
            Secure Workspace
          </div>

          <h1>Welcome back</h1>

          <p>
            Select your role to continue to your personalized workspace.
          </p>
        </div>

        <div className="role-grid">
          {roles.map((role) => {
            const Icon = role.icon;
            const selected = selectedRole === role.id;

            return (
              <button
                key={role.id}
                type="button"
                className={`role-card ${role.accent} ${
                  selected ? "selected" : ""
                }`}
                onClick={() => setSelectedRole(role.id)}
              >
                <div className="role-card-top">
                  <div className="role-icon">
                    <Icon size={24} />
                  </div>

                  <div className="role-radio">
                    <span />
                  </div>
                </div>

                <div className="role-card-content">
                  <h2>{role.title}</h2>
                  <p>{role.description}</p>
                </div>

                <div className="role-card-footer">
                  <span>Select {role.title}</span>
                  <ArrowRight size={16} />
                </div>
              </button>
            );
          })}
        </div>

        <button
          className="role-continue"
          disabled={!selectedRole}
          onClick={continueToLogin}
        >
          Continue
          <ArrowRight size={17} />
        </button>

        <p className="role-security-note">
          <ShieldCheck size={14} />
          Your workspace access is protected by role-based authentication.
        </p>

        <div className="role-footer">
          <span>© 2026 AI Loss Prevention System</span>
          <span>Secure • Private • Intelligent</span>
        </div>
      </section>
    </main>
  );
}

export default RoleSelection;