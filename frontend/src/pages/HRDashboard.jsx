import { useEffect, useState } from "react";
import {
  LayoutDashboard,
  Users,
  FolderKanban,
  CheckSquare,
  Brain,
  Activity,
  Settings,
  HelpCircle,
  Search,
  Bell,
  RefreshCw,
  ShieldCheck,
  Clock3,
  Send,
  Bot,
  FileText,
  LogOut,
} from "lucide-react";
import "./HRDashboard.css";

const API = "http://127.0.0.1:8000";


// ============================================================
// AUTH
// ============================================================

const getToken = () => {
  return localStorage.getItem("auth_token");
};


const logout = () => {
  localStorage.removeItem("auth_token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("user_identifier");
  localStorage.removeItem("remember_me");

  window.location.href = "/";
};


// ============================================================
// AUTHENTICATED API REQUEST
// ============================================================

const authFetch = async (url, options = {}) => {
  const token = getToken();

  if (!token) {
    logout();
    throw new Error("Authentication required.");
  }

  const response = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  });

  if (response.status === 401 || response.status === 403) {
    localStorage.removeItem("auth_token");

    window.location.href = "/login?role=hr";

    throw new Error("Authentication expired.");
  }

  return response;
};


function HRDashboard() {

  // ============================================================
  // AUTH CHECK
  // ============================================================

  useEffect(() => {
    const token = getToken();
    const role = localStorage.getItem("user_role");

    if (!token || role !== "hr") {
      window.location.href = "/login?role=hr";
    }
  }, []);


  // ============================================================
  // PAGE
  // ============================================================

  const [activePage, setActivePage] = useState("dashboard");


  // ============================================================
  // DATA
  // ============================================================

  const [overview, setOverview] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [projects, setProjects] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [activities, setActivities] = useState([]);
  const [knowledgeCount, setKnowledgeCount] = useState(0);


  // ============================================================
  // LOADING / ERROR
  // ============================================================

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  // ============================================================
  // AI
  // ============================================================

  const [aiQuestion, setAiQuestion] = useState("");
  const [aiMessages, setAiMessages] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");


  // ============================================================
  // API JSON
  // ============================================================

  const apiJson = async (url, options = {}) => {

    const response = await authFetch(
      url,
      options
    );

    const data =
      await response
        .json()
        .catch(() => ({}));


    if (!response.ok) {
      throw new Error(
        data.detail ||
        data.message ||
        "Request failed."
      );
    }

    return data;
  };


  // ============================================================
  // LOAD OVERVIEW
  // ============================================================

  const loadOverview = async () => {

    const data =
      await apiJson(
        `${API}/hr/overview`
      );

    setOverview(data);

    setKnowledgeCount(
      data.team_knowledge || 0
    );

  };


  // ============================================================
  // LOAD EMPLOYEES
  // ============================================================

  const loadEmployees = async () => {

    const data =
      await apiJson(
        `${API}/hr/employees`
      );

    setEmployees(
      data.employees || []
    );

  };


  // ============================================================
  // LOAD PROJECTS
  // ============================================================

  const loadProjects = async () => {

    const data =
      await apiJson(
        `${API}/hr/projects`
      );

    setProjects(
      data.projects || []
    );

  };


  // ============================================================
  // LOAD TASKS
  // ============================================================

  const loadTasks = async () => {

    const data =
      await apiJson(
        `${API}/hr/tasks`
      );

    setTasks(
      data.tasks || []
    );

  };


  // ============================================================
  // LOAD ACTIVITY
  // ============================================================

  const loadActivities = async () => {

    const data =
      await apiJson(
        `${API}/hr/activity`
      );

    setActivities(
      data.activities || []
    );

  };


  // ============================================================
  // REFRESH EVERYTHING
  // ============================================================

  const refreshAll = async () => {

    setLoading(true);
    setError("");

    try {

      await Promise.all([
        loadOverview(),
        loadEmployees(),
        loadProjects(),
        loadTasks(),
        loadActivities(),
      ]);

    } catch (err) {

      console.error(err);

      if (
        err.message !==
          "Authentication expired." &&
        err.message !==
          "Authentication required."
      ) {
        setError(
          err.message ||
          "Unable to load HR data."
        );
      }

    } finally {

      setLoading(false);

    }

  };


  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {

    const token = getToken();
    const role =
      localStorage.getItem(
        "user_role"
      );

    if (
      token &&
      role === "hr"
    ) {
      refreshAll();
    }

  }, []);


  // ============================================================
  // OPEN PAGE
  // ============================================================

  const openPage = async (page) => {

    setActivePage(page);

    setError("");

    try {

      if (page === "dashboard") {
        await loadOverview();
      }

      if (page === "employees") {
        await loadEmployees();
      }

      if (page === "projects") {
        await loadProjects();
      }

      if (page === "tasks") {
        await loadTasks();
      }

      if (page === "activity") {
        await loadActivities();
      }

    } catch (err) {

      console.error(err);

      if (
        err.message !==
          "Authentication expired." &&
        err.message !==
          "Authentication required."
      ) {

        setError(
          err.message ||
          "Unable to load data."
        );

      }

    }

  };


  // ============================================================
  // NAVIGATION
  // ============================================================

  const navItems = [

    {
      id: "dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
    },

    {
      id: "employees",
      label: "Employees",
      icon: Users,
    },

    {
      id: "projects",
      label: "Projects",
      icon: FolderKanban,
    },

    {
      id: "tasks",
      label: "Tasks",
      icon: CheckSquare,
    },

    {
      id: "knowledge",
      label: "Team Knowledge",
      icon: Brain,
    },

    {
      id: "ai",
      label: "AI Assistant",
      icon: Bot,
    },

    {
      id: "activity",
      label: "Activity",
      icon: Activity,
    },

    {
      id: "settings",
      label: "Settings",
      icon: Settings,
    },

    {
      id: "help",
      label: "Help & Support",
      icon: HelpCircle,
    },

  ];


  // ============================================================
  // AI ASSISTANT
  // ============================================================

  const askAI = async (
    question = aiQuestion
  ) => {

    const trimmed =
      question.trim();

    if (
      !trimmed ||
      aiLoading
    ) {
      return;
    }


    setAiQuestion("");
    setAiError("");


    setAiMessages(
      (previous) => [
        ...previous,
        {
          role: "user",
          content: trimmed,
        },
      ]
    );


    setAiLoading(true);


    try {

      const response =
        await authFetch(
          `${API}/ask`,
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              question: trimmed,
            }),

          }
        );


      const data =
        await response
          .json()
          .catch(
            () => ({})
          );


      if (!response.ok) {

        throw new Error(
          data.detail ||
          data.message ||
          "AI request failed."
        );

      }


      const answer =
        data.answer ||
        data.response ||
        data.message ||
        "No answer returned.";


      setAiMessages(
        (previous) => [
          ...previous,
          {
            role: "assistant",
            content: answer,
          },
        ]
      );


    } catch (err) {

      console.error(err);

      if (
        err.message !==
        "Authentication expired."
      ) {

        setAiError(
          err.message ||
          "Unable to connect to AI Assistant."
        );

      }

    } finally {

      setAiLoading(false);

    }

  };


  // ============================================================
  // AI ENTER KEY
  // ============================================================

  const handleAIKeyDown = (
    event
  ) => {

    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {

      event.preventDefault();

      askAI();

    }

  };


  // ============================================================
  // AI PAGE
  // ============================================================

  const renderAI = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>


          <div className="hr-ai-page-title">

            <div className="hr-ai-page-icon">
              <Bot size={24} />
            </div>


            <div>

              <h1>
                AI Assistant
              </h1>

              <p>
                Ask questions about employees,
                projects, tasks and available
                organizational knowledge.
              </p>

            </div>

          </div>

        </div>


        <span className="hr-ai-online">

          <span className="hr-ai-online-dot" />

          AI Ready

        </span>

      </section>


      <section className="hr-ai-assistant-card">

        <div className="hr-ai-assistant-header">

          <div className="hr-ai-assistant-avatar">
            <Bot size={20} />
          </div>


          <div>

            <h3>
              HR AI
            </h3>

            <p>
              Powered by the existing RAG / Ask pipeline
            </p>

          </div>

        </div>


        <div className="hr-ai-suggestions">

          <span>
            Quick questions
          </span>


          <button
            onClick={() =>
              askAI(
                "Show total employees"
              )
            }
          >

            <Users size={14} />

            Total employees

          </button>


          <button
            onClick={() =>
              askAI(
                "Show active projects"
              )
            }
          >

            <FolderKanban size={14} />

            Active projects

          </button>


          <button
            onClick={() =>
              askAI(
                "Show pending tasks"
              )
            }
          >

            <CheckSquare size={14} />

            Pending tasks

          </button>


          <button
            onClick={() =>
              askAI(
                "Summarize recent team activity"
              )
            }
          >

            <Activity size={14} />

            Team activity

          </button>


          <button
            onClick={() =>
              askAI(
                "What team knowledge is available?"
              )
            }
          >

            <Brain size={14} />

            Team knowledge

          </button>

        </div>


        <div className="hr-ai-conversation">

          {aiMessages.length === 0 &&
          !aiLoading ? (

            <div className="hr-ai-empty">

              <div className="hr-ai-empty-icon">
                <Bot size={30} />
              </div>

              <h3>
                How can I help?
              </h3>

              <p>
                Ask a question about your
                organization, or choose one of
                the quick questions above.
              </p>

            </div>

          ) : (

            aiMessages.map(
              (message, index) => (

                <div
                  className={`hr-ai-message ${message.role}`}
                  key={`${message.role}-${index}`}
                >

                  <div className="hr-ai-message-avatar">

                    {message.role ===
                    "assistant" ? (
                      <Bot size={15} />
                    ) : (
                      <Users size={15} />
                    )}

                  </div>


                  <div className="hr-ai-bubble">

                    <span className="hr-ai-message-role">

                      {message.role ===
                      "assistant"
                        ? "HR AI"
                        : "You"}

                    </span>


                    <div>
                      {message.content}
                    </div>

                  </div>

                </div>

              )
            )

          )}


          {aiLoading && (

            <div className="hr-ai-message assistant">

              <div className="hr-ai-message-avatar">
                <Bot size={15} />
              </div>


              <div className="hr-ai-bubble">

                <span className="hr-ai-message-role">
                  HR AI
                </span>


                <div className="hr-ai-typing">

                  <span />
                  <span />
                  <span />

                </div>

              </div>

            </div>

          )}

        </div>


        {aiError && (

          <div className="hr-ai-error">
            {aiError}
          </div>

        )}


        <div className="hr-ai-composer">

          <textarea
            value={aiQuestion}
            onChange={(event) =>
              setAiQuestion(
                event.target.value
              )
            }
            onKeyDown={
              handleAIKeyDown
            }
            placeholder="Ask your question..."
            rows={2}
            disabled={aiLoading}
          />


          <button
            className="hr-ai-send"
            onClick={() =>
              askAI()
            }
            disabled={
              aiLoading ||
              !aiQuestion.trim()
            }
          >

            <Send size={17} />

            Ask AI

          </button>

        </div>

      </section>

    </>

  );


  // ============================================================
  // DASHBOARD
  // ============================================================

  const renderDashboard = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            HR Dashboard
          </h1>

          <p>
            Organization-wide visibility
            into employees, projects and work.
          </p>

        </div>


        <button
          className="hr-primary-button"
          onClick={refreshAll}
        >

          <RefreshCw size={16} />

          {loading
            ? "Refreshing..."
            : "Refresh"}

        </button>

      </section>


      <section className="hr-stats">


        <div className="hr-stat-card">

          <div className="hr-stat-icon blue">
            <Users size={19} />
          </div>

          <span>
            Total Employees
          </span>

          <strong>
            {overview?.total_employees ?? 0}
          </strong>

          <small>
            Employees across projects
          </small>

        </div>


        <div className="hr-stat-card">

          <div className="hr-stat-icon purple">
            <FolderKanban size={19} />
          </div>

          <span>
            Total Projects
          </span>

          <strong>
            {overview?.total_projects ?? 0}
          </strong>

          <small>
            Active organization projects
          </small>

        </div>


        <div className="hr-stat-card">

          <div className="hr-stat-icon orange">
            <CheckSquare size={19} />
          </div>

          <span>
            Pending Tasks
          </span>

          <strong>
            {overview?.pending_tasks ?? 0}
          </strong>

          <small>
            {overview?.total_tasks ?? 0}
            {" "}
            total tasks
          </small>

        </div>


        <div className="hr-stat-card">

          <div className="hr-stat-icon green">
            <Brain size={19} />
          </div>

          <span>
            Team Knowledge
          </span>

          <strong>
            {knowledgeCount}
          </strong>

          <small>
            Knowledge records
          </small>

        </div>

      </section>


      <section className="hr-dashboard-grid">


        <div className="hr-card">

          <div className="hr-card-header">

            <div>

              <h3>
                Employees
              </h3>

              <p>
                Current employees working
                across projects.
              </p>

            </div>


            <button
              className="hr-link-button"
              onClick={() =>
                openPage(
                  "employees"
                )
              }
            >

              View All

            </button>

          </div>


          <div className="hr-mini-list">

            {employees
              .slice(0, 5)
              .map(
                (employee) => (

                  <div
                    className="hr-mini-row"
                    key={
                      employee.employee_id
                    }
                  >

                    <div className="hr-mini-avatar">
                      {employee.employee_id.slice(-1)}
                    </div>


                    <div>

                      <strong>
                        {employee.employee_id}
                      </strong>

                      <span>
                        {employee.project_count}
                        {" "}
                        project
                        {employee.project_count === 1
                          ? ""
                          : "s"}
                      </span>

                    </div>


                    <span className="hr-active-badge">
                      Active
                    </span>

                  </div>

                )
              )}


            {employees.length === 0 && (

              <div className="hr-empty">
                No employees found.
              </div>

            )}

          </div>

        </div>


        <div className="hr-card">

          <div className="hr-card-header">

            <div>

              <h3>
                Recent Activity
              </h3>

              <p>
                Latest organization activity.
              </p>

            </div>


            <button
              className="hr-link-button"
              onClick={() =>
                openPage(
                  "activity"
                )
              }
            >

              View All

            </button>

          </div>


          <div className="hr-mini-list">

            {activities
              .slice(0, 5)
              .map(
                (item, index) => (

                  <div
                    className="hr-mini-row"
                    key={`${item.timestamp}-${index}`}
                  >

                    <div
                      className={`hr-mini-icon ${
                        item.type ||
                        "default"
                      }`}
                    >

                      {item.type ===
                        "task" && (
                        <CheckSquare
                          size={16}
                        />
                      )}

                      {item.type ===
                        "project" && (
                        <FolderKanban
                          size={16}
                        />
                      )}

                      {item.type ===
                        "employee" && (
                        <Users
                          size={16}
                        />
                      )}

                      {item.type ===
                        "knowledge" && (
                        <Brain
                          size={16}
                        />
                      )}

                    </div>


                    <div>

                      <strong>
                        {item.title}
                      </strong>

                      <span>
                        {item.description}
                      </span>

                    </div>

                  </div>

                )
              )}


            {activities.length === 0 && (

              <div className="hr-empty">
                No activity found.
              </div>

            )}

          </div>

        </div>

      </section>

    </>

  );


  // ============================================================
  // EMPLOYEES
  // ============================================================

  const renderEmployees = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            Employees
          </h1>

          <p>
            Organization-wide employee
            overview.
          </p>

        </div>


        <button
          className="hr-primary-button"
          onClick={
            loadEmployees
          }
        >

          <RefreshCw size={16} />

          Refresh

        </button>

      </section>


      <section className="hr-employee-grid">

        {employees.map(
          (employee) => (

            <article
              className="hr-employee-card"
              key={
                employee.employee_id
              }
            >

              <div className="hr-employee-top">

                <div className="hr-employee-avatar">
                  {employee.employee_id.slice(-1)}
                </div>


                <span className="hr-active-badge">
                  Active
                </span>

              </div>


              <h2>
                {employee.employee_id}
              </h2>


              <p>
                Employee account connected
                to the project workspace.
              </p>


              <div className="hr-employee-metrics">

                <div>

                  <strong>
                    {employee.project_count}
                  </strong>

                  <span>
                    Projects
                  </span>

                </div>


                <div>

                  <strong>
                    {employee.task_count}
                  </strong>

                  <span>
                    Tasks
                  </span>

                </div>


                <div>

                  <strong>
                    {employee.knowledge_count}
                  </strong>

                  <span>
                    Knowledge
                  </span>

                </div>

              </div>


              <div className="hr-divider" />


              <h4>
                Projects
              </h4>


              <div className="hr-project-tags">

                {employee.projects?.map(
                  (project) => (

                    <span
                      key={
                        project.id
                      }
                    >
                      {project.name}
                    </span>

                  )
                )}


                {(!employee.projects ||
                  employee.projects.length === 0) && (

                  <small>
                    No projects assigned.
                  </small>

                )}

              </div>

            </article>

          )
        )}


        {employees.length === 0 && (

          <div className="hr-empty-large">

            <Users size={34} />

            <h3>
              No employees found
            </h3>

            <p>
              Employee records will appear
              here when they are assigned
              to projects.
            </p>

          </div>

        )}

      </section>

    </>

  );


  // ============================================================
  // PROJECTS
  // ============================================================

  const renderProjects = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            Projects
          </h1>

          <p>
            View all organization projects
            and their team sizes.
          </p>

        </div>


        <button
          className="hr-primary-button"
          onClick={
            loadProjects
          }
        >

          <RefreshCw size={16} />

          Refresh

        </button>

      </section>


      <section className="hr-project-grid">

        {projects.map(
          (project) => (

            <article
              className="hr-project-card"
              key={project.id}
            >

              <div className="hr-project-top">

                <div className="hr-project-icon">
                  <FolderKanban size={20} />
                </div>


                <span className="hr-active-badge">
                  {project.status ||
                    "Active"}
                </span>

              </div>


              <h2>
                {project.name}
              </h2>


              <p>
                {project.description ||
                  "No description provided."}
              </p>


              <div className="hr-project-info">

                <div>

                  <span>
                    Manager
                  </span>

                  <strong>
                    {project.manager_id}
                  </strong>

                </div>


                <div>

                  <span>
                    Employees
                  </span>

                  <strong>
                    {project.employee_count}
                  </strong>

                </div>


                <div>

                  <span>
                    Tasks
                  </span>

                  <strong>
                    {project.task_count}
                  </strong>

                </div>

              </div>


              <div className="hr-divider" />


              <h4>
                Team
              </h4>


              <div className="hr-project-tags">

                {project.employees?.map(
                  (employee) => (

                    <span
                      key={employee}
                    >
                      {employee}
                    </span>

                  )
                )}


                {(!project.employees ||
                  project.employees.length === 0) && (

                  <small>
                    No employees assigned.
                  </small>

                )}

              </div>

            </article>

          )
        )}


        {projects.length === 0 && (

          <div className="hr-empty-large">

            <FolderKanban size={34} />

            <h3>
              No projects found
            </h3>

            <p>
              Projects will appear
              here automatically.
            </p>

          </div>

        )}

      </section>

    </>

  );


  // ============================================================
  // TASKS
  // ============================================================

  const renderTasks = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            All Tasks
          </h1>

          <p>
            Organization-wide task
            visibility.
          </p>

        </div>


        <button
          className="hr-primary-button"
          onClick={
            loadTasks
          }
        >

          <RefreshCw size={16} />

          Refresh

        </button>

      </section>


      <section className="hr-table-card">

        <div className="hr-table-header">

          <span>Task</span>
          <span>Employee</span>
          <span>Manager</span>
          <span>Priority</span>
          <span>Status</span>
          <span>Due Date</span>

        </div>


        {tasks.map(
          (task) => (

            <div
              className="hr-table-row"
              key={task.id}
            >

              <div>

                <strong>
                  {task.title}
                </strong>

                <small>
                  {task.description ||
                    "No description."}
                </small>

              </div>


              <span>
                {task.employee_id}
              </span>


              <span>
                {task.manager_id}
              </span>


              <span className="hr-priority-badge">
                {task.priority}
              </span>


              <span className="hr-status-pill">
                {task.status}
              </span>


              <span>

                {task.due_date
                  ? new Date(
                      task.due_date
                    ).toLocaleDateString(
                      "en-IN"
                    )
                  : "—"}

              </span>

            </div>

          )
        )}


        {tasks.length === 0 && (

          <div className="hr-empty">
            No tasks found.
          </div>

        )}

      </section>

    </>

  );


  // ============================================================
  // KNOWLEDGE
  // ============================================================

  const renderKnowledge = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            Team Knowledge
          </h1>

          <p>
            Organization knowledge count
            and system-level visibility.
          </p>

        </div>


        <button
          className="hr-primary-button"
          onClick={
            loadOverview
          }
        >

          <RefreshCw size={16} />

          Refresh

        </button>

      </section>


      <section className="hr-knowledge-summary">

        <div className="hr-knowledge-big-icon">
          <Brain size={28} />
        </div>


        <div>

          <span>
            Total Team Knowledge
          </span>

          <strong>
            {knowledgeCount}
          </strong>

          <p>
            Knowledge records currently
            associated with active project
            employees.
          </p>

        </div>

      </section>


      <section className="hr-card hr-knowledge-note">

        <FileText size={20} />


        <div>

          <h3>
            Privacy-aware visibility
          </h3>

          <p>
            HR sees organization-level
            knowledge metrics. Sensitive
            knowledge content is not exposed
            through this HR overview.
          </p>

        </div>

      </section>

    </>

  );


  // ============================================================
  // ACTIVITY
  // ============================================================

  const renderActivity = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            Activity
          </h1>

          <p>
            Recent organization activity
            across projects and tasks.
          </p>

        </div>


        <button
          className="hr-primary-button"
          onClick={
            loadActivities
          }
        >

          <RefreshCw size={16} />

          Refresh

        </button>

      </section>


      <section className="hr-activity-card">

        {activities.map(
          (item, index) => (

            <article
              className="hr-activity-row"
              key={`${item.timestamp}-${index}`}
            >

              <div
                className={`hr-activity-icon ${
                  item.type ||
                  "default"
                }`}
              >

                {item.type ===
                  "task" && (
                  <CheckSquare
                    size={18}
                  />
                )}

                {item.type ===
                  "project" && (
                  <FolderKanban
                    size={18}
                  />
                )}

                {item.type ===
                  "employee" && (
                  <Users
                    size={18}
                  />
                )}

                {item.type ===
                  "knowledge" && (
                  <Brain
                    size={18}
                  />
                )}

                {![
                  "task",
                  "project",
                  "employee",
                  "knowledge",
                ].includes(
                  item.type
                ) && (
                  <Activity
                    size={18}
                  />
                )}

              </div>


              <div className="hr-activity-content">

                <strong>
                  {item.title}
                </strong>

                <span>
                  {item.description}
                </span>

                <small>

                  {item.timestamp
                    ? new Date(
                        item.timestamp
                      ).toLocaleString(
                        "en-IN"
                      )
                    : "—"}

                </small>

              </div>

            </article>

          )
        )}


        {activities.length === 0 && (

          <div className="hr-empty-large">

            <Activity size={34} />

            <h3>
              No activity found
            </h3>

            <p>
              Recent organization events
              will appear here.
            </p>

          </div>

        )}

      </section>

    </>

  );


  // ============================================================
  // SETTINGS
  // ============================================================

  const renderSettings = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            Settings
          </h1>

          <p>
            HR workspace configuration
            and system information.
          </p>

        </div>

      </section>


      <section className="hr-settings-card">

        <div className="hr-settings-icon">
          <ShieldCheck size={22} />
        </div>


        <div>

          <h3>
            HR Access
          </h3>

          <p>
            Organization-wide
            read-only visibility
          </p>

          <strong>
            HR Workspace
          </strong>

        </div>

      </section>


      <section className="hr-settings-card">

        <div className="hr-settings-icon">
          <Clock3 size={22} />
        </div>


        <div>

          <h3>
            System Status
          </h3>

          <p>
            Manager and HR API
            connectivity
          </p>

          <strong className="hr-online">
            Connected
          </strong>

        </div>

      </section>

    </>

  );


  // ============================================================
  // HELP
  // ============================================================

  const renderHelp = () => (

    <>

      <section className="hr-page-heading">

        <div>

          <span className="hr-eyebrow">
            Human Resources
          </span>

          <h1>
            Help & Support
          </h1>

          <p>
            Quick guidance for the
            HR workspace.
          </p>

        </div>

      </section>


      <section className="hr-help-grid">

        <article className="hr-help-card">

          <Users size={19} />

          <div>

            <h3>
              Employees
            </h3>

            <p>
              View employees and their
              project, task and knowledge
              counts.
            </p>

          </div>

        </article>


        <article className="hr-help-card">

          <FolderKanban size={19} />

          <div>

            <h3>
              Projects
            </h3>

            <p>
              Review projects, managers
              and assigned team members.
            </p>

          </div>

        </article>


        <article className="hr-help-card">

          <CheckSquare size={19} />

          <div>

            <h3>
              Tasks
            </h3>

            <p>
              Monitor organization-wide
              task status, priority and
              due dates.
            </p>

          </div>

        </article>


        <article className="hr-help-card">

          <Activity size={19} />

          <div>

            <h3>
              Activity
            </h3>

            <p>
              Track recent project,
              employee and task events.
            </p>

          </div>

        </article>

      </section>

    </>

  );


  // ============================================================
  // MAIN UI
  // ============================================================

  return (

    <div className="hr-shell">


      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="hr-sidebar">


        <div className="hr-brand">

          <div className="hr-brand-logo">
            AI
          </div>


          <div>

            <strong>
              RABC System
            </strong>

            <span>
              HR Workspace
            </span>

          </div>

        </div>


        <nav className="hr-nav">

          {navItems.map(
            ({
              id,
              label,
              icon: Icon,
            }) => (

              <button
                key={id}
                className={`hr-nav-item ${
                  activePage === id
                    ? "active"
                    : ""
                }`}
                onClick={() =>
                  openPage(id)
                }
              >

                <Icon size={18} />

                <span>
                  {label}
                </span>

              </button>

            )
          )}

        </nav>


        <div className="hr-ai-card">

          <div className="hr-ai-title">

            <Brain size={16} />

            HR Insights

          </div>


          <p>
            Organization-level visibility
            into people, projects and work.
          </p>


          <button
            onClick={() =>
              openPage(
                "employees"
              )
            }
          >

            View Employees

            <span>
              ↗
            </span>

          </button>

        </div>


        {/* ====================================================
            PROFILE
        ==================================================== */}

        <div className="hr-profile-bottom">

          <div className="hr-avatar">
            HR
          </div>


          <div>

            <strong>
              Human Resources
            </strong>

            <span>
              HR Workspace
            </span>

          </div>

        </div>


        {/* ====================================================
            LOGOUT
        ==================================================== */}

        <button
          type="button"
          className="hr-logout-button"
          onClick={logout}
        >

          <LogOut size={17} />

          <span>
            Logout
          </span>

        </button>


      </aside>


      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="hr-main">


        <header className="hr-topbar">


          <div className="hr-search">

            <Search size={18} />

            <input
              placeholder="Search..."
            />

          </div>


          <div className="hr-top-actions">


            <button className="hr-notification">

              <Bell size={20} />

              <span />

            </button>


            <div className="hr-top-profile">

              <div className="hr-avatar">
                HR
              </div>


              <div>

                <strong>
                  Human Resources
                </strong>

                <span>
                  HR Workspace
                </span>

              </div>

            </div>


            {/* =================================================
                TOP LOGOUT
            ================================================= */}

            <button
              type="button"
              className="hr-top-logout"
              onClick={logout}
              title="Logout"
            >

              <LogOut size={18} />

            </button>


          </div>

        </header>


        {/* ====================================================
            ERROR
        ==================================================== */}

        {error && (

          <div className="hr-error">

            {error}

          </div>

        )}


        <div className="hr-content">

          {activePage ===
            "dashboard" &&
            renderDashboard()}


          {activePage ===
            "employees" &&
            renderEmployees()}


          {activePage ===
            "projects" &&
            renderProjects()}


          {activePage ===
            "tasks" &&
            renderTasks()}


          {activePage ===
            "knowledge" &&
            renderKnowledge()}


          {activePage ===
            "ai" &&
            renderAI()}


          {activePage ===
            "activity" &&
            renderActivity()}


          {activePage ===
            "settings" &&
            renderSettings()}


          {activePage ===
            "help" &&
            renderHelp()}

        </div>

      </main>

    </div>

  );

}


export default HRDashboard;