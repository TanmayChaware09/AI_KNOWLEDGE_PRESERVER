import { useEffect, useState } from "react";

import {
  Home,
  BookOpen,
  Upload,
  CheckSquare,
  Bot,
  BarChart3,
  Settings,
  HelpCircle,
  Search,
  Bell,
  FileText,
  Users,
  ClipboardList,
  Sparkles,
  ArrowUpRight,
  Plus,
  Clock3,
  Eye,
  Send,
  X,
} from "lucide-react";

import "./EmployeeDashboard.css";


function EmployeeDashboard() {

  // ============================================================
  // TIME-BASED GREETING
  // ============================================================

  const currentHour = new Date().getHours();

  const greeting =
    currentHour < 12
      ? "Good Morning"
      : currentHour < 17
        ? "Good Afternoon"
        : "Good Evening";


  // ============================================================
  // AI ASSISTANT STATE
  // ============================================================

  const [showAssistant, setShowAssistant] = useState(false);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [loading, setLoading] = useState(false);


  // ============================================================
  // MY KNOWLEDGE STATE
  // ============================================================

  const [activePage, setActivePage] = useState("dashboard");

  const [knowledge, setKnowledge] = useState([]);

  const [knowledgeLoading, setKnowledgeLoading] = useState(false);

  const [knowledgeError, setKnowledgeError] = useState("");

  const [knowledgeSearch, setKnowledgeSearch] = useState("");

  const [knowledgeCategory, setKnowledgeCategory] = useState("All");


  // ============================================================
  // UPLOAD KNOWLEDGE STATE
  // ============================================================

  const [selectedFile, setSelectedFile] = useState(null);

  const [uploadingKnowledge, setUploadingKnowledge] = useState(false);

  const [uploadMessage, setUploadMessage] = useState("");

  const [uploadError, setUploadError] = useState("");


  // ============================================================
  // MY TASKS STATE
  // ============================================================

  const [tasks, setTasks] = useState([]);

  const [tasksLoading, setTasksLoading] = useState(false);

  const [tasksError, setTasksError] = useState("");


  // ============================================================
  // SETTINGS STATE
  // ============================================================

  const [notificationsEnabled, setNotificationsEnabled] = useState(true);

  const [aiSuggestionsEnabled, setAiSuggestionsEnabled] = useState(true);


  // ============================================================
  // LOAD MY KNOWLEDGE
  // ============================================================

  const loadKnowledge = async () => {

    setKnowledgeLoading(true);
    setKnowledgeError("");

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/knowledge"
      );

      if (!response.ok) {
        throw new Error("Knowledge API request failed");
      }

      const data = await response.json();

      setKnowledge(
        Array.isArray(data.knowledge)
          ? data.knowledge
          : []
      );

    } catch (error) {

      console.error(
        "My Knowledge Error:",
        error
      );

      setKnowledgeError(
        "Unable to load your knowledge."
      );

    } finally {

      setKnowledgeLoading(false);

    }
  };


  useEffect(() => {

    if (activePage === "knowledge") {
      loadKnowledge();
    }

    if (activePage === "tasks") {
      loadTasks();
    }

    if (activePage === "reports") {
      loadKnowledge();
      loadTasks();
    }

  }, [activePage]);


  // ============================================================
  // KNOWLEDGE FILTERING
  // ============================================================

  const categories = [
    "All",
    ...new Set(
      knowledge
        .map((item) => item.category)
        .filter(Boolean)
    ),
  ];

  const filteredKnowledge = knowledge.filter(
    (item) => {

      const searchText =
        knowledgeSearch
          .trim()
          .toLowerCase();

      const matchesSearch =
        !searchText ||
        item.title
          ?.toLowerCase()
          .includes(searchText) ||
        item.summary
          ?.toLowerCase()
          .includes(searchText);

      const matchesCategory =
        knowledgeCategory === "All" ||
        item.category === knowledgeCategory;

      return (
        matchesSearch &&
        matchesCategory
      );

    }
  );


  // ============================================================
  // LOAD MY TASKS
  // ============================================================

  const loadTasks = async () => {

    setTasksLoading(true);
    setTasksError("");

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/tasks?employee_id=EMP001"
      );

      if (!response.ok) {
        throw new Error("Tasks API request failed");
      }

      const data = await response.json();

      setTasks(
        Array.isArray(data.tasks)
          ? data.tasks
          : []
      );

    } catch (error) {

      console.error(
        "My Tasks Error:",
        error
      );

      setTasksError(
        "Unable to load your tasks."
      );

    } finally {

      setTasksLoading(false);

    }
  };


  // ============================================================
  // UPLOAD KNOWLEDGE
  // ============================================================

  const uploadKnowledge = async () => {

    if (!selectedFile) {

      setUploadError(
        "Please select a .txt file first."
      );

      return;
    }


    setUploadingKnowledge(true);
    setUploadMessage("");
    setUploadError("");


    try {

      const formData = new FormData();

      formData.append(
        "file",
        selectedFile
      );

      // Temporary development identity.
      // Later this will come from authenticated RBAC login.
      formData.append(
        "employee_id",
        "EMP001"
      );

      formData.append(
        "employee_name",
        "Rohit"
      );

      formData.append(
        "department",
        "Engineering"
      );


      const response = await fetch(
        "http://127.0.0.1:8000/upload",
        {
          method: "POST",
          body: formData,
        }
      );


      const data = await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Upload failed."
        );

      }


      if (!data.success) {

        throw new Error(
          data.message ||
          "No knowledge was stored."
        );

      }


      setUploadMessage(
        `${data.stored} knowledge card${
          data.stored === 1 ? "" : "s"
        } uploaded successfully.`
      );


      setSelectedFile(null);


      // Refresh My Knowledge immediately.
      await loadKnowledge();


    } catch (error) {

      console.error(
        "Upload Knowledge Error:",
        error
      );

      setUploadError(
        error.message ||
        "Unable to upload knowledge."
      );

    } finally {

      setUploadingKnowledge(false);

    }

  };


  // ============================================================
  // PAGE NAVIGATION
  // ============================================================

  const openPage = (page) => {

    setActivePage(page);

  };


  // ============================================================
  // ASK AI ASSISTANT
  // ============================================================

  const askAssistant = async () => {

    if (!question.trim()) {
      return;
    }

    setLoading(true);
    setAnswer("");

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question: question.trim(),
          }),
        }
      );


      if (!response.ok) {
        throw new Error("API request failed");
      }


      const data = await response.json();


      setAnswer(
        data.answer ||
        "No answer received."
      );


    } catch (error) {

      console.error(
        "AI Assistant Error:",
        error
      );


      setAnswer(
        "Unable to connect to the AI Assistant."
      );


    } finally {

      setLoading(false);

    }
  };


  // ============================================================
  // OPEN ASSISTANT
  // ============================================================

  const openAssistant = () => {

    setShowAssistant(true);

  };


  // ============================================================
  // CLOSE ASSISTANT
  // ============================================================

  const closeAssistant = () => {

    setShowAssistant(false);

  };


  // ============================================================
  // MAIN UI
  // ============================================================

  return (

    <div className="employee-dashboard">

      <style>{`
        .employee-dashboard {
          font-size: 16px;
        }
        .employee-dashboard h1 {
          font-size: 34px !important;
          line-height: 1.2;
        }
        .employee-dashboard h3 {
          font-size: 21px !important;
        }
        .employee-dashboard h4 {
          font-size: 16px !important;
        }
        .employee-dashboard p {
          font-size: 14px !important;
          line-height: 1.55;
        }
        .employee-dashboard .employee-nav-item,
        .employee-dashboard .employee-nav-section,
        .employee-dashboard .employee-profile,
        .employee-dashboard .employee-search input,
        .employee-dashboard button,
        .employee-dashboard label {
          font-size: 14px !important;
        }
        .employee-dashboard .stat-card-top span,
        .employee-dashboard .stat-change,
        .employee-dashboard .stat-description,
        .employee-dashboard .activity-content span,
        .employee-dashboard .activity-time,
        .employee-dashboard .view-all-button {
          font-size: 13px !important;
        }
        .employee-dashboard .stat-number {
          font-size: 34px !important;
        }
      `}</style>


      {/* =====================================================
          SIDEBAR
      ===================================================== */}

      <aside className="employee-sidebar">


        {/* BRAND */}

        <div className="employee-brand">

          <div className="employee-brand-icon">

            <BookOpen size={22} />

          </div>


          <div>

            <h2>
              RABC System
            </h2>

            <span>
              AI Knowledge Risk Prevention
            </span>

          </div>

        </div>


        {/* NAVIGATION */}

        <nav className="employee-navigation">


          <button
            className={
              activePage === "dashboard"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("dashboard")}
          >

            <Home size={18} />

            <span>
              Dashboard
            </span>

          </button>


          <button
            className={
              activePage === "knowledge" ||
              activePage === "upload"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("knowledge")}
          >

            <BookOpen size={18} />

            <span>
              My Knowledge
            </span>

          </button>


          <button
            className={
              activePage === "upload"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("upload")}
          >

            <Upload size={18} />

            <span>
              Upload Knowledge
            </span>

          </button>


          <button
            className={
              activePage === "tasks"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("tasks")}
          >

            <CheckSquare size={18} />

            <span>
              My Tasks
            </span>

          </button>


          {/* AI ASSISTANT NAV */}

          <button
            className="employee-nav-item"
            onClick={openAssistant}
          >

            <Bot size={18} />

            <span>
              AI Assistant
            </span>

          </button>


          <button
            className={
              activePage === "reports"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("reports")}
          >

            <BarChart3 size={18} />

            <span>
              Reports
            </span>

          </button>


          <div className="employee-nav-section">

            <span>
              OTHER
            </span>

          </div>


          <button
            className={
              activePage === "settings"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("settings")}
          >

            <Settings size={18} />

            <span>
              Settings
            </span>

          </button>


          <button
            className={
              activePage === "help"
                ? "employee-nav-item active"
                : "employee-nav-item"
            }
            onClick={() => openPage("help")}
          >

            <HelpCircle size={18} />

            <span>
              Help & Support
            </span>

          </button>


        </nav>


        {/* =====================================================
            SIDEBAR AI CARD
        ===================================================== */}

        <div className="sidebar-ai-card">


          <div className="sidebar-ai-header">

            <div className="sidebar-ai-icon">

              <Sparkles size={16} />

            </div>


            <span>
              AI Assistant
            </span>

          </div>


          <p>
            Ask anything about your knowledge and projects.
          </p>


          <button
            className="sidebar-ai-button"
            onClick={openAssistant}
          >

            Ask a question

            <ArrowUpRight size={14} />

          </button>


        </div>


      </aside>


      {/* =====================================================
          MAIN CONTENT
      ===================================================== */}

      <main className="employee-main">


        {/* =====================================================
            TOP BAR
        ===================================================== */}

        <header className="employee-topbar">


          <div className="employee-search">

            <Search size={18} />

            <input
              type="text"
              placeholder="Search knowledge, documents..."
            />

          </div>


          <div className="employee-top-actions">


            <button
              className="notification-button"
            >

              <Bell size={19} />

              <span
                className="notification-dot"
              />

            </button>


            <div className="employee-profile">


              <div className="profile-avatar">
                RS
              </div>


              <div className="profile-details">

                <strong>
                  Rohit Singh
                </strong>

                <span>
                  Employee
                </span>

              </div>


              <span className="profile-arrow">
                ▼
              </span>


            </div>


          </div>


        </header>


        {activePage === "dashboard" && (

          <>

        {/* =====================================================
            PAGE HEADING
        ===================================================== */}

        <section className="employee-welcome">


          <div>

            <h1>
              {greeting}, Rohit 👋
            </h1>


            <p>
              Here's what's happening with your knowledge today.
            </p>

          </div>


          <label
            className="quick-upload-button"
            style={{ cursor: "pointer" }}
          >

            <Plus size={17} />

            Upload Knowledge

            <input
              type="file"
              accept=".txt,text/plain"
              style={{ display: "none" }}
              onChange={(event) => {

                const file =
                  event.target.files?.[0];

                if (file) {

                  setSelectedFile(file);
                  setUploadMessage("");
                  setUploadError("");
                  openPage("upload");

                }

              }}
            />

          </label>


        </section>


        {/* =====================================================
            STATISTICS
        ===================================================== */}

        <section className="employee-stats">

          <div className="employee-stat-card">
            <div className="stat-card-top">
              <span>My Knowledge</span>
              <div className="stat-icon blue"><BookOpen size={20} /></div>
            </div>
            <div className="stat-number">{knowledge.length}</div>
            <div className="stat-description">
              Privacy-processed knowledge cards
            </div>
          </div>

          <div className="employee-stat-card">
            <div className="stat-card-top">
              <span>Tasks Assigned</span>
              <div className="stat-icon green"><ClipboardList size={20} /></div>
            </div>
            <div className="stat-number">{tasks.length}</div>
            <div className="stat-description">
              Tasks assigned to you
            </div>
          </div>

          <div className="employee-stat-card">
            <div className="stat-card-top">
              <span>Pending Tasks</span>
              <div className="stat-icon orange"><Clock3 size={20} /></div>
            </div>
            <div className="stat-number">
              {tasks.filter(
                (task) => (task.status || "").toLowerCase() === "pending"
              ).length}
            </div>
            <div className="stat-description">
              Tasks waiting to be completed
            </div>
          </div>

          <div className="employee-stat-card">
            <div className="stat-card-top">
              <span>Completed Tasks</span>
              <div className="stat-icon purple"><CheckSquare size={20} /></div>
            </div>
            <div className="stat-number">
              {tasks.filter(
                (task) => (task.status || "").toLowerCase() === "completed"
              ).length}
            </div>
            <div className="stat-description">
              Tasks completed by you
            </div>
          </div>

        </section>


        {/* =====================================================
            ACTIVITY + KNOWLEDGE FLOW
        ===================================================== */}

        <section className="employee-middle-grid">


          {/* RECENT ACTIVITY */}

          <div className="dashboard-card activity-card">

            <div className="dashboard-card-header">
              <div>
                <h3>Recent Activity</h3>
                <p>Your latest knowledge and task activity</p>
              </div>

              <button
                className="view-all-button"
                onClick={() => openPage("knowledge")}
              >
                View Knowledge
              </button>
            </div>

            <div className="activity-list">

              {[
                ...knowledge.slice(0, 3).map((item) => ({
                  key: `knowledge-${item.id}`,
                  title: item.title || "Knowledge added",
                  description: "Knowledge stored after privacy processing",
                  time: item.timestamp
                    ? new Date(item.timestamp).toLocaleDateString()
                    : "Recent",
                  icon: "knowledge",
                })),
                ...tasks.slice(0, 3).map((task) => ({
                  key: `task-${task.id}`,
                  title: task.title,
                  description: `Task status: ${task.status || "Pending"}`,
                  time: task.due_date
                    ? `Due ${new Date(task.due_date).toLocaleDateString()}`
                    : "No due date",
                  icon: "task",
                })),
              ].slice(0, 5).map((item) => (

                <div className="activity-item" key={item.key}>

                  <div
                    className={
                      item.icon === "task"
                        ? "activity-icon purple"
                        : "activity-icon blue"
                    }
                  >
                    {item.icon === "task"
                      ? <CheckSquare size={18} />
                      : <BookOpen size={18} />}
                  </div>

                  <div className="activity-content">
                    <strong>{item.title}</strong>
                    <span>{item.description}</span>
                  </div>

                  <span className="activity-time">
                    {item.time}
                  </span>

                </div>

              ))}

              {knowledge.length === 0 && tasks.length === 0 && (
                <div
                  style={{
                    padding: "28px 10px",
                    textAlign: "center",
                    color: "#697586",
                  }}
                >
                  No recent activity yet.
                </div>
              )}

            </div>

          </div>


          {/* =====================================================
              KNOWLEDGE FLOW
          ===================================================== */}

          <div className="dashboard-card knowledge-flow-card">


            <div className="dashboard-card-header">


              <div>

                <h3>
                  My Work Flow
                </h3>

                <p>
                  Knowledge contributions and assigned work
                </p>

              </div>


              <select className="week-select">

                <option>
                  This Week
                </option>

                <option>
                  Last Week
                </option>

                <option>
                  This Month
                </option>

              </select>


            </div>


            <div className="knowledge-chart">


              <div className="chart-y-axis">

                <span>80</span>
                <span>60</span>
                <span>40</span>
                <span>20</span>
                <span>0</span>

              </div>


              <div className="chart-area">


                <div className="chart-grid-line line-1" />
                <div className="chart-grid-line line-2" />
                <div className="chart-grid-line line-3" />
                <div className="chart-grid-line line-4" />


                <svg
                  className="knowledge-line"
                  viewBox="0 0 500 180"
                  preserveAspectRatio="none"
                >


                  <defs>

                    <linearGradient
                      id="knowledgeGradient"
                      x1="0"
                      x2="0"
                      y1="0"
                      y2="1"
                    >

                      <stop
                        offset="0%"
                        stopColor="#2563eb"
                        stopOpacity="0.25"
                      />

                      <stop
                        offset="100%"
                        stopColor="#2563eb"
                        stopOpacity="0"
                      />

                    </linearGradient>

                  </defs>


                  <path
                    d="
                      M0 130
                      C35 85, 60 110, 95 100
                      C130 90, 140 120, 175 105
                      C210 90, 225 125, 260 85
                      C300 45, 315 65, 350 35
                      C380 10, 405 70, 430 82
                      C455 95, 475 70, 500 55
                      L500 180
                      L0 180
                      Z
                    "
                    fill="url(#knowledgeGradient)"
                  />


                  <path
                    d="
                      M0 130
                      C35 85, 60 110, 95 100
                      C130 90, 140 120, 175 105
                      C210 90, 225 125, 260 85
                      C300 45, 315 65, 350 35
                      C380 10, 405 70, 430 82
                      C455 95, 475 70, 500 55
                    "
                    fill="none"
                    stroke="#2563eb"
                    strokeWidth="3"
                  />


                </svg>


                <div className="chart-days">

                  <span>Mon</span>
                  <span>Tue</span>
                  <span>Wed</span>
                  <span>Thu</span>
                  <span>Fri</span>
                  <span>Sat</span>
                  <span>Sun</span>

                </div>


              </div>


            </div>


          </div>


        </section>




          </>

        )}


        {/* =====================================================
            REPORTS PAGE
        ===================================================== */}

        {activePage === "reports" && (

          <section className="dashboard-card my-knowledge-card">

            <div className="dashboard-card-header">

              <div>

                <h3>
                  My Work Report
                </h3>

                <p>
                  A summary of your own work and contributions.
                </p>

              </div>

              <button
                className="view-all-button"
                onClick={() => {
                  loadKnowledge();
                  loadTasks();
                }}
              >
                Refresh
              </button>

            </div>


            <div
              style={{
                display: "grid",
                gridTemplateColumns:
                  "repeat(auto-fit, minmax(170px, 1fr))",
                gap: "14px",
                marginBottom: "22px",
              }}
            >

              <div style={{
                padding: "18px",
                border: "1px solid #e6eaf0",
                borderRadius: "12px",
                background: "#ffffff",
              }}>
                <BookOpen size={19} />
                <div style={{
                  marginTop: "12px",
                  fontSize: "24px",
                  fontWeight: 700,
                  color: "#273142",
                }}>
                  {knowledge.length}
                </div>
                <div style={{
                  marginTop: "4px",
                  fontSize: "11px",
                  color: "#7b8699",
                }}>
                  Knowledge Contributions
                </div>
              </div>


              <div style={{
                padding: "18px",
                border: "1px solid #e6eaf0",
                borderRadius: "12px",
                background: "#ffffff",
              }}>
                <CheckSquare size={19} />
                <div style={{
                  marginTop: "12px",
                  fontSize: "24px",
                  fontWeight: 700,
                  color: "#273142",
                }}>
                  {tasks.filter(
                    (task) =>
                      (task.status || "").toLowerCase() ===
                      "completed"
                  ).length}
                </div>
                <div style={{
                  marginTop: "4px",
                  fontSize: "11px",
                  color: "#7b8699",
                }}>
                  Tasks Completed
                </div>
              </div>


              <div style={{
                padding: "18px",
                border: "1px solid #e6eaf0",
                borderRadius: "12px",
                background: "#ffffff",
              }}>
                <Clock3 size={19} />
                <div style={{
                  marginTop: "12px",
                  fontSize: "24px",
                  fontWeight: 700,
                  color: "#273142",
                }}>
                  {tasks.filter(
                    (task) =>
                      (task.status || "").toLowerCase() ===
                      "pending"
                  ).length}
                </div>
                <div style={{
                  marginTop: "4px",
                  fontSize: "11px",
                  color: "#7b8699",
                }}>
                  Tasks Pending
                </div>
              </div>


              <div style={{
                padding: "18px",
                border: "1px solid #e6eaf0",
                borderRadius: "12px",
                background: "#ffffff",
              }}>
                <BarChart3 size={19} />
                <div style={{
                  marginTop: "12px",
                  fontSize: "24px",
                  fontWeight: 700,
                  color: "#273142",
                }}>
                  {tasks.filter(
                    (task) =>
                      (task.status || "").toLowerCase() ===
                      "in progress"
                  ).length}
                </div>
                <div style={{
                  marginTop: "4px",
                  fontSize: "11px",
                  color: "#7b8699",
                }}>
                  In Progress
                </div>
              </div>

            </div>


            <div
              style={{
                padding: "18px",
                border: "1px solid #e6eaf0",
                borderRadius: "12px",
                background: "#ffffff",
              }}
            >

              <h4 style={{
                margin: "0 0 14px",
                color: "#273142",
                fontSize: "15px",
              }}>
                Recent Work
              </h4>


              {knowledge.length === 0 && tasks.length === 0 ? (

                <div style={{
                  padding: "28px 10px",
                  textAlign: "center",
                  color: "#7b8699",
                  fontSize: "12px",
                }}>
                  No work activity available yet.
                </div>

              ) : (

                <div style={{
                  display: "grid",
                  gap: "10px",
                }}>

                  {tasks.slice(0, 4).map((task) => (

                    <div
                      key={`task-${task.id}`}
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: "12px",
                        padding: "12px",
                        borderRadius: "9px",
                        background: "#f8fafc",
                      }}
                    >

                      <div>
                        <div style={{
                          fontSize: "12px",
                          fontWeight: 600,
                          color: "#344054",
                        }}>
                          {task.title}
                        </div>

                        <div style={{
                          marginTop: "3px",
                          fontSize: "10px",
                          color: "#7b8699",
                        }}>
                          Task • {task.status || "Pending"}
                        </div>
                      </div>

                      <CheckSquare
                        size={16}
                        style={{ flexShrink: 0 }}
                      />

                    </div>

                  ))}


                  {knowledge.slice(0, 4).map((item) => (

                    <div
                      key={`knowledge-${item.id}`}
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        gap: "12px",
                        padding: "12px",
                        borderRadius: "9px",
                        background: "#f8fafc",
                      }}
                    >

                      <div>
                        <div style={{
                          fontSize: "12px",
                          fontWeight: 600,
                          color: "#344054",
                        }}>
                          {item.title}
                        </div>

                        <div style={{
                          marginTop: "3px",
                          fontSize: "10px",
                          color: "#7b8699",
                        }}>
                          Knowledge Contribution
                        </div>
                      </div>

                      <BookOpen
                        size={16}
                        style={{ flexShrink: 0 }}
                      />

                    </div>

                  ))}

                </div>

              )}

            </div>

          </section>

        )}


        {/* =====================================================
            MY TASKS PAGE
        ===================================================== */}

        {activePage === "tasks" && (

          <section className="dashboard-card my-knowledge-card">

            <div className="dashboard-card-header">

              <div>

                <h3>
                  My Tasks
                </h3>

                <p>
                  Tasks assigned to you by your manager.
                </p>

              </div>

              <button
                className="view-all-button"
                onClick={loadTasks}
                disabled={tasksLoading}
              >
                {tasksLoading ? "Refreshing..." : "Refresh"}
              </button>

            </div>


            {tasksError && (

              <div
                style={{
                  padding: "14px",
                  marginBottom: "16px",
                  borderRadius: "9px",
                  background: "#fff4f4",
                  color: "#c24141",
                  fontSize: "13px",
                }}
              >
                {tasksError}
              </div>

            )}


            {tasksLoading && (

              <div
                style={{
                  padding: "45px 20px",
                  textAlign: "center",
                  color: "#7b8699",
                  fontSize: "13px",
                }}
              >
                Loading your tasks...
              </div>

            )}


            {!tasksLoading &&
              !tasksError &&
              tasks.length === 0 && (

                <div
                  style={{
                    padding: "50px 20px",
                    textAlign: "center",
                    color: "#7b8699",
                    fontSize: "13px",
                  }}
                >

                  <CheckSquare
                    size={30}
                    style={{
                      marginBottom: "10px",
                      opacity: 0.55,
                    }}
                  />

                  <div>
                    No tasks assigned to you.
                  </div>

                </div>

              )}


            {!tasksLoading &&
              !tasksError &&
              tasks.length > 0 && (

                <div
                  style={{
                    display: "grid",
                    gap: "14px",
                  }}
                >

                  {tasks.map((task) => {

                    const priority =
                      (task.priority || "medium")
                        .toLowerCase();

                    const status =
                      (task.status || "pending")
                        .toLowerCase();

                    const priorityLabel =
                      priority.charAt(0).toUpperCase() +
                      priority.slice(1);

                    const statusLabel =
                      status.charAt(0).toUpperCase() +
                      status.slice(1);

                    return (

                      <article
                        key={task.id}
                        style={{
                          padding: "18px",
                          border: "1px solid #e6eaf0",
                          borderRadius: "12px",
                          background: "#ffffff",
                        }}
                      >

                        <div
                          style={{
                            display: "flex",
                            justifyContent: "space-between",
                            alignItems: "flex-start",
                            gap: "14px",
                          }}
                        >

                          <div
                            style={{
                              display: "flex",
                              gap: "12px",
                              minWidth: 0,
                            }}
                          >

                            <div
                              style={{
                                width: "38px",
                                height: "38px",
                                display: "flex",
                                alignItems: "center",
                                justifyContent: "center",
                                borderRadius: "9px",
                                background: "#eef4ff",
                                color: "#2563eb",
                                flexShrink: 0,
                              }}
                            >
                              <CheckSquare size={18} />
                            </div>


                            <div>

                              <h4
                                style={{
                                  margin: "0 0 7px",
                                  color: "#273142",
                                  fontSize: "15px",
                                  lineHeight: 1.4,
                                }}
                              >
                                {task.title}
                              </h4>

                              <p
                                style={{
                                  margin: 0,
                                  color: "#697586",
                                  fontSize: "12px",
                                  lineHeight: 1.55,
                                }}
                              >
                                {task.description ||
                                  "No description provided."}
                              </p>

                            </div>

                          </div>


                          <span
                            style={{
                              padding: "5px 9px",
                              borderRadius: "999px",
                              background:
                                priority === "high"
                                  ? "#fff0f0"
                                  : "#f3f5f8",
                              color:
                                priority === "high"
                                  ? "#c24141"
                                  : "#667085",
                              fontSize: "10px",
                              fontWeight: 700,
                              whiteSpace: "nowrap",
                            }}
                          >
                            {priorityLabel}
                          </span>

                        </div>


                        <div
                          style={{
                            display: "flex",
                            flexWrap: "wrap",
                            gap: "10px",
                            alignItems: "center",
                            marginTop: "16px",
                            paddingTop: "13px",
                            borderTop: "1px solid #eef1f5",
                          }}
                        >

                          <span
                            style={{
                              padding: "5px 9px",
                              borderRadius: "999px",
                              background: "#f3f5f8",
                              color: "#667085",
                              fontSize: "10px",
                              fontWeight: 600,
                            }}
                          >
                            {statusLabel}
                          </span>


                          <span
                            style={{
                              color: "#7b8699",
                              fontSize: "10px",
                            }}
                          >
                            Due:{" "}
                            {task.due_date
                              ? new Date(
                                  task.due_date
                                ).toLocaleDateString()
                              : "No due date"}
                          </span>

                        </div>

                      </article>

                    );

                  })}

                </div>

              )}

          </section>

        )}


        {/* =====================================================
            SETTINGS PAGE
        ===================================================== */}

        {activePage === "settings" && (

          <section className="dashboard-card my-knowledge-card">

            <div className="dashboard-card-header">

              <div>
                <h3>Settings</h3>
                <p>Manage your employee dashboard preferences.</p>
              </div>

            </div>


            <div
              style={{
                display: "grid",
                gap: "14px",
              }}
            >

              <div
                style={{
                  padding: "18px",
                  border: "1px solid #e6eaf0",
                  borderRadius: "12px",
                  background: "#ffffff",
                }}
              >

                <h4 style={{
                  margin: "0 0 6px",
                  color: "#273142",
                  fontSize: "15px",
                }}>
                  Profile
                </h4>

                <p style={{
                  margin: 0,
                  color: "#697586",
                  fontSize: "12px",
                }}>
                  Rohit • Engineering • Employee
                </p>

              </div>


              <div
                style={{
                  padding: "18px",
                  border: "1px solid #e6eaf0",
                  borderRadius: "12px",
                  background: "#ffffff",
                }}
              >

                <h4 style={{
                  margin: "0 0 14px",
                  color: "#273142",
                  fontSize: "15px",
                }}>
                  Preferences
                </h4>


                <label
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "12px 0",
                    borderBottom: "1px solid #eef1f5",
                    fontSize: "12px",
                    color: "#344054",
                  }}
                >
                  Notifications
                  <input
                    type="checkbox"
                    checked={notificationsEnabled}
                    onChange={(e) =>
                      setNotificationsEnabled(e.target.checked)
                    }
                  />
                </label>


                <label
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "12px 0",
                    fontSize: "12px",
                    color: "#344054",
                  }}
                >
                  AI Suggestions
                  <input
                    type="checkbox"
                    checked={aiSuggestionsEnabled}
                    onChange={(e) =>
                      setAiSuggestionsEnabled(e.target.checked)
                    }
                  />
                </label>

              </div>


              <div
                style={{
                  padding: "14px 18px",
                  borderRadius: "10px",
                  background: "#f8fafc",
                  color: "#697586",
                  fontSize: "11px",
                }}
              >
                Your privacy-protected knowledge is processed through the
                existing privacy pipeline before RAG storage.
              </div>

            </div>

          </section>

        )}


        {/* =====================================================
            HELP & SUPPORT PAGE
        ===================================================== */}

        {activePage === "help" && (

          <section className="dashboard-card my-knowledge-card">

            <div className="dashboard-card-header">

              <div>
                <h3>Help & Support</h3>
                <p>Quick answers for using your employee workspace.</p>
              </div>

            </div>


            <div style={{
              display: "grid",
              gap: "12px",
            }}>

              {[
                {
                  question: "How does My Knowledge work?",
                  answer:
                    "Your stored knowledge is retrieved from the knowledge system and shown in your employee workspace."
                },
                {
                  question: "Is uploaded private information sent directly to RAG?",
                  answer:
                    "No. Uploaded knowledge passes through the privacy pipeline before it is stored for retrieval."
                },
                {
                  question: "Where can I see assigned work?",
                  answer:
                    "Open My Tasks from the sidebar to see your assigned tasks, priorities and due dates."
                },
                {
                  question: "How do I ask the AI Assistant?",
                  answer:
                    "Open AI Assistant and ask a question about your available project knowledge."
                },
              ].map((item) => (

                <div
                  key={item.question}
                  style={{
                    padding: "16px",
                    border: "1px solid #e6eaf0",
                    borderRadius: "11px",
                    background: "#ffffff",
                  }}
                >

                  <h4 style={{
                    margin: "0 0 7px",
                    color: "#273142",
                    fontSize: "13px",
                  }}>
                    {item.question}
                  </h4>

                  <p style={{
                    margin: 0,
                    color: "#697586",
                    fontSize: "11px",
                    lineHeight: 1.55,
                  }}>
                    {item.answer}
                  </p>

                </div>

              ))}


              <div
                style={{
                  padding: "16px",
                  borderRadius: "11px",
                  background: "#eef4ff",
                  color: "#344054",
                  fontSize: "12px",
                }}
              >
                <strong>Need more help?</strong>
                <br />
                Contact your manager or system administrator for
                account, access or project-specific issues.
              </div>

            </div>

          </section>

        )}


        {/* =====================================================
            UPLOAD KNOWLEDGE PAGE
        ===================================================== */}

        {activePage === "upload" && (

          <section className="dashboard-card my-knowledge-card">

            <div className="dashboard-card-header">

              <div>

                <h3>
                  Upload Knowledge
                </h3>

                <p>
                  Upload a text document to extract and securely store knowledge.
                </p>

              </div>

              <button
                className="view-all-button"
                onClick={() => openPage("knowledge")}
              >
                My Knowledge
              </button>

            </div>


            <div
              style={{
                padding: "24px",
                border: "1px dashed #cfd6e0",
                borderRadius: "12px",
                background: "#fafbfc",
              }}
            >

              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  textAlign: "center",
                  gap: "10px",
                }}
              >

                <div
                  style={{
                    width: "52px",
                    height: "52px",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    borderRadius: "12px",
                    background: "#eef4ff",
                    color: "#2563eb",
                  }}
                >
                  <Upload size={23} />
                </div>


                <h4
                  style={{
                    margin: "4px 0 0",
                    fontSize: "17px",
                    color: "#273142",
                  }}
                >
                  Upload a knowledge file
                </h4>


                <p
                  style={{
                    margin: 0,
                    fontSize: "12px",
                    color: "#697586",
                  }}
                >
                  Currently supported: UTF-8 .txt files
                </p>


                <label
                  style={{
                    marginTop: "8px",
                    padding: "10px 16px",
                    borderRadius: "8px",
                    background: "#eef4ff",
                    color: "#2563eb",
                    fontSize: "12px",
                    fontWeight: 600,
                    cursor: "pointer",
                  }}
                >

                  Choose File

                  <input
                    type="file"
                    accept=".txt,text/plain"
                    style={{ display: "none" }}
                    onChange={(event) => {

                      const file =
                        event.target.files?.[0];

                      if (file) {

                        setSelectedFile(file);
                        setUploadMessage("");
                        setUploadError("");

                      }

                    }}
                  />

                </label>


                {selectedFile && (

                  <div
                    style={{
                      marginTop: "8px",
                      padding: "10px 14px",
                      borderRadius: "8px",
                      background: "#ffffff",
                      border: "1px solid #e5e9ef",
                      color: "#344054",
                      fontSize: "12px",
                    }}
                  >
                    Selected:{" "}
                    <strong>
                      {selectedFile.name}
                    </strong>
                  </div>

                )}


                <button
                  type="button"
                  onClick={uploadKnowledge}
                  disabled={
                    !selectedFile ||
                    uploadingKnowledge
                  }
                  style={{
                    marginTop: "6px",
                    minWidth: "150px",
                    padding: "11px 18px",
                    border: "none",
                    borderRadius: "8px",
                    background:
                      !selectedFile ||
                      uploadingKnowledge
                        ? "#cfd6e0"
                        : "#2563eb",
                    color: "#ffffff",
                    fontSize: "12px",
                    fontWeight: 600,
                    cursor:
                      !selectedFile ||
                      uploadingKnowledge
                        ? "not-allowed"
                        : "pointer",
                  }}
                >
                  {uploadingKnowledge
                    ? "Processing..."
                    : "Upload Knowledge"}
                </button>


                {uploadMessage && (

                  <div
                    style={{
                      marginTop: "8px",
                      padding: "10px 14px",
                      borderRadius: "8px",
                      background: "#edf9f0",
                      color: "#27743a",
                      fontSize: "12px",
                    }}
                  >
                    {uploadMessage}
                  </div>

                )}


                {uploadError && (

                  <div
                    style={{
                      marginTop: "8px",
                      padding: "10px 14px",
                      borderRadius: "8px",
                      background: "#fff4f4",
                      color: "#c24141",
                      fontSize: "12px",
                    }}
                  >
                    {uploadError}
                  </div>

                )}

              </div>

            </div>

          </section>

        )}


        {/* =====================================================
            MY KNOWLEDGE PAGE
        ===================================================== */}

        {activePage === "knowledge" && (

          <section className="dashboard-card my-knowledge-card">

            <div className="dashboard-card-header">

              <div>

                <h3>
                  My Knowledge
                </h3>

                <p>
                  Knowledge captured and stored from your work.
                </p>

              </div>

              <button
                className="view-all-button"
                onClick={loadKnowledge}
                disabled={knowledgeLoading}
              >
                {knowledgeLoading ? "Refreshing..." : "Refresh"}
              </button>

            </div>


            <div
              style={{
                display: "flex",
                gap: "12px",
                marginBottom: "20px",
                flexWrap: "wrap",
              }}
            >

              <div
                style={{
                  flex: "1",
                  minWidth: "220px",
                  position: "relative",
                }}
              >

                <Search
                  size={17}
                  style={{
                    position: "absolute",
                    left: "12px",
                    top: "50%",
                    transform: "translateY(-50%)",
                    color: "#8a94a6",
                  }}
                />

                <input
                  type="text"
                  value={knowledgeSearch}
                  onChange={(event) =>
                    setKnowledgeSearch(event.target.value)
                  }
                  placeholder="Search your knowledge..."
                  style={{
                    width: "100%",
                    height: "42px",
                    padding: "0 12px 0 38px",
                    border: "1px solid #dfe4eb",
                    borderRadius: "9px",
                    outline: "none",
                    fontSize: "13px",
                    boxSizing: "border-box",
                  }}
                />

              </div>


              <select
                value={knowledgeCategory}
                onChange={(event) =>
                  setKnowledgeCategory(event.target.value)
                }
                style={{
                  height: "42px",
                  minWidth: "150px",
                  padding: "0 12px",
                  border: "1px solid #dfe4eb",
                  borderRadius: "9px",
                  background: "#ffffff",
                  color: "#344054",
                  fontSize: "13px",
                  outline: "none",
                }}
              >

                {categories.map((category) => (

                  <option
                    key={category}
                    value={category}
                  >
                    {category}
                  </option>

                ))}

              </select>

            </div>


            {knowledgeError && (

              <div
                style={{
                  padding: "14px",
                  marginBottom: "16px",
                  borderRadius: "9px",
                  background: "#fff4f4",
                  color: "#c24141",
                  fontSize: "13px",
                }}
              >
                {knowledgeError}
              </div>

            )}


            {knowledgeLoading && (

              <div
                style={{
                  padding: "45px 20px",
                  textAlign: "center",
                  color: "#7b8699",
                  fontSize: "13px",
                }}
              >
                Loading your knowledge...
              </div>

            )}


            {!knowledgeLoading &&
              !knowledgeError &&
              filteredKnowledge.length === 0 && (

                <div
                  style={{
                    padding: "50px 20px",
                    textAlign: "center",
                    color: "#7b8699",
                    fontSize: "13px",
                  }}
                >

                  <BookOpen
                    size={30}
                    style={{
                      marginBottom: "10px",
                      opacity: 0.55,
                    }}
                  />

                  <div>
                    No knowledge found.
                  </div>

                </div>

              )}


            {!knowledgeLoading &&
              filteredKnowledge.length > 0 && (

                <div
                  style={{
                    display: "grid",
                    gridTemplateColumns:
                      "repeat(auto-fit, minmax(280px, 1fr))",
                    gap: "16px",
                  }}
                >

                  {filteredKnowledge.map((item) => (

                    <article
                      key={item.id}
                      style={{
                        padding: "18px",
                        border: "1px solid #e6eaf0",
                        borderRadius: "12px",
                        background: "#ffffff",
                        minHeight: "175px",
                        boxSizing: "border-box",
                      }}
                    >

                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "flex-start",
                          gap: "10px",
                          marginBottom: "12px",
                        }}
                      >

                        <div
                          style={{
                            width: "38px",
                            height: "38px",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                            borderRadius: "9px",
                            background: "#eef4ff",
                            color: "#2563eb",
                            flexShrink: 0,
                          }}
                        >

                          <BookOpen size={18} />

                        </div>


                        {item.category && (

                          <span
                            style={{
                              padding: "5px 9px",
                              borderRadius: "999px",
                              background: "#f3f5f8",
                              color: "#667085",
                              fontSize: "10px",
                              fontWeight: 600,
                            }}
                          >
                            {item.category}
                          </span>

                        )}

                      </div>


                      <h4
                        style={{
                          margin: "0 0 8px",
                          color: "#273142",
                          fontSize: "15px",
                          lineHeight: 1.4,
                        }}
                      >
                        {item.title}
                      </h4>


                      <p
                        style={{
                          margin: "0 0 15px",
                          color: "#697586",
                          fontSize: "12px",
                          lineHeight: 1.55,
                        }}
                      >
                        {item.summary}
                      </p>


                      <div
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          alignItems: "center",
                          gap: "10px",
                          paddingTop: "12px",
                          borderTop: "1px solid #eef1f5",
                        }}
                      >

                        <span
                          style={{
                            color: "#7b8699",
                            fontSize: "10px",
                          }}
                        >
                          {item.timestamp
                            ? new Date(
                                item.timestamp
                              ).toLocaleDateString()
                            : "No date"}
                        </span>


                        <span
                          style={{
                            color: "#2563eb",
                            fontSize: "10px",
                            fontWeight: 600,
                          }}
                        >
                          Confidence:{" "}
                          {typeof item.confidence === "number"
                            ? `${Math.round(
                                item.confidence * 100
                              )}%`
                            : "N/A"}
                        </span>

                      </div>

                    </article>

                  ))}

                </div>

              )}

          </section>

        )}


        {/* =====================================================
            AI ASSISTANT PANEL
        ===================================================== */}

        {showAssistant && (

          <div className="ai-assistant-overlay">


            <div className="ai-assistant-panel">


              {/* HEADER */}

              <div className="ai-assistant-header">


                <div className="ai-assistant-title">


                  <div className="ai-assistant-avatar">

                    <Bot size={20} />

                  </div>


                  <div>

                    <h3>
                      AI Assistant
                    </h3>

                    <span>
                      Knowledge Assistant
                    </span>

                  </div>


                </div>


                <button
                  className="ai-close-button"
                  onClick={closeAssistant}
                >

                  <X size={19} />

                </button>


              </div>


              {/* CHAT BODY */}

              <div className="ai-assistant-body">


                {!question && !answer && !loading && (

                  <div className="ai-welcome-message">


                    <div className="ai-welcome-icon">

                      <Sparkles size={24} />

                    </div>


                    <h3>
                      How can I help you?
                    </h3>


                    <p>
                      Ask me about your projects, knowledge,
                      decisions, or work updates.
                    </p>


                  </div>

                )}


                {/* USER QUESTION */}

                {question && (

                  <div className="chat-message user-message">


                    <span className="message-label">
                      You
                    </span>


                    <div className="message-bubble">
                      {question}
                    </div>


                  </div>

                )}


                {/* LOADING */}

                {loading && (

                  <div className="chat-message assistant-message">


                    <span className="message-label">
                      AI Assistant
                    </span>


                    <div className="message-bubble">
                      Searching your knowledge...
                    </div>


                  </div>

                )}


                {/* ANSWER */}

                {answer && !loading && (

                  <div className="chat-message assistant-message">


                    <span className="message-label">
                      AI Assistant
                    </span>


                    <div className="message-bubble">
                      {answer}
                    </div>


                  </div>

                )}


              </div>


              {/* INPUT */}

              <div className="ai-assistant-input-area">


                <input
                  type="text"
                  value={question}
                  onChange={(event) =>
                    setQuestion(event.target.value)
                  }
                  onKeyDown={(event) => {

                    if (
                      event.key === "Enter" &&
                      !loading
                    ) {

                      askAssistant();

                    }

                  }}
                  placeholder="Ask about your knowledge..."
                  disabled={loading}
                />


                <button
                  onClick={askAssistant}
                  disabled={
                    loading ||
                    !question.trim()
                  }
                >

                  <Send size={17} />

                </button>


              </div>


            </div>


          </div>

        )}


        {/* =====================================================
            FLOATING AI BUTTON
        ===================================================== */}

        <button
          className="floating-ai-button"
          onClick={openAssistant}
        >

          <Bot size={23} />

        </button>


      </main>


    </div>

  );

}


export default EmployeeDashboard;