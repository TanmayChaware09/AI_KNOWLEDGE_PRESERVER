import {
  ArrowRight,
  BrainCircuit,
  ShieldCheck,
  UsersRound,
  Database,
  Sparkles,
  LockKeyhole,
} from "lucide-react";
import "./LandingPage.css";

function LandingPage() {
  const getStarted = () => {
    window.location.href = "/roles";
  };

  return (
    <main className="landing-page">
      <div className="landing-orb landing-orb-one" />
      <div className="landing-orb landing-orb-two" />

      <nav className="landing-nav">
        <div className="landing-brand">
          <div className="landing-brand-icon">
            <Sparkles size={19} />
          </div>

          <div>
            <strong>AI Loss Prevention</strong>
            <span>Intelligent Knowledge System</span>
          </div>
        </div>

        <div className="landing-nav-status">
          <span className="landing-status-dot" />
          Secure Workspace
        </div>
      </nav>

      <section className="landing-hero">
        <div className="landing-badge">
          <Sparkles size={14} />
          AI-Powered Enterprise Protection
        </div>

        <h1>
          Preserve your organization's
          <span> knowledge.</span>
        </h1>

        <p className="landing-description">
          An intelligent loss prevention platform that brings together
          organizational knowledge, privacy, projects and people in one
          secure workspace.
        </p>

        <div className="landing-actions">
          <button className="landing-primary-btn" onClick={getStarted}>
            Get Started
            <ArrowRight size={17} />
          </button>

          <div className="landing-security">
            <ShieldCheck size={15} />
            Role-based secure access
          </div>
        </div>
      </section>

      <section className="landing-features">
        <div className="landing-section-heading">
          <span>BUILT FOR MODERN TEAMS</span>
          <h2>Everything your organization needs.</h2>
        </div>

        <div className="landing-feature-grid">
          <article className="landing-feature-card">
            <div className="landing-feature-icon blue">
              <BrainCircuit size={22} />
            </div>
            <h3>AI Knowledge</h3>
            <p>
              Turn valuable organizational knowledge into an intelligent,
              searchable knowledge system.
            </p>
          </article>

          <article className="landing-feature-card">
            <div className="landing-feature-icon purple">
              <LockKeyhole size={22} />
            </div>
            <h3>Privacy First</h3>
            <p>
              Protect sensitive information with privacy-aware processing
              before knowledge reaches the AI layer.
            </p>
          </article>

          <article className="landing-feature-card">
            <div className="landing-feature-icon green">
              <UsersRound size={22} />
            </div>
            <h3>Role Based Access</h3>
            <p>
              Employees, managers and HR get personalized workspaces based
              on their authorized role.
            </p>
          </article>

          <article className="landing-feature-card">
            <div className="landing-feature-icon orange">
              <Database size={22} />
            </div>
            <h3>Centralized Intelligence</h3>
            <p>
              Connect people, projects, tasks and organizational knowledge
              through one intelligent platform.
            </p>
          </article>
        </div>
      </section>

      <section className="landing-cta">
        <div>
          <span>ONE SECURE WORKSPACE</span>
          <h2>Make organizational knowledge work for you.</h2>
        </div>

        <button onClick={getStarted}>
          Enter Workspace
          <ArrowRight size={16} />
        </button>
      </section>

      <footer className="landing-footer">
        <span>© 2026 AI Loss Prevention System</span>

        <div>
          <span>Secure</span>
          <span>Private</span>
          <span>Intelligent</span>
        </div>
      </footer>
    </main>
  );
}

export default LandingPage;