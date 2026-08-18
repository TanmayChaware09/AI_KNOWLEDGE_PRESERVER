import { useEffect, useState } from "react";

import {
  LayoutDashboard,
  FolderKanban,
  CheckSquare,
  Brain,
  Activity,
  Settings,
  HelpCircle,
  Search,
  Bell,
  Users,
  ClipboardList,
  Plus,
  Clock3,
  CheckCircle2,
  UserPlus,
  RefreshCw,
  X,
  ArrowUpRight,
  Trash2,
  MessageCircle,
  Send,
  Sparkles,
} from "lucide-react";

import "./ManagerDashboard.css";


// ============================================================
// CONFIG
// ============================================================

const API_BASE = "http://127.0.0.1:8000";

const MANAGER_ID = "MANAGER001";


// ============================================================
// GREETING
// ============================================================

function getGreeting() {

  const hour = new Date().getHours();

  if (hour < 12) {
    return "Good Morning";
  }

  if (hour < 17) {
    return "Good Afternoon";
  }

  return "Good Evening";
}


// ============================================================
// MAIN COMPONENT
// ============================================================

function ManagerDashboard() {


  // ============================================================
  // NAVIGATION
  // ============================================================

  const [activePage, setActivePage] =
    useState("Dashboard");


  // ============================================================
  // DASHBOARD DATA
  // ============================================================

  const [overview, setOverview] =
    useState(null);

  const [projects, setProjects] =
    useState([]);

  const [tasks, setTasks] =
    useState([]);

  const [teamKnowledge, setTeamKnowledge] =
    useState([]);

  const [activities, setActivities] =
    useState([]);


  // ============================================================
  // LOADING / ERROR
  // ============================================================

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [submitting, setSubmitting] =
    useState(false);


  // ============================================================
  // AI ASSISTANT
  // ============================================================

  const [aiQuestion, setAiQuestion] =
    useState("");

  const [aiAnswer, setAiAnswer] =
    useState("");

  const [aiLoading, setAiLoading] =
    useState(false);

  const [aiError, setAiError] =
    useState("");

  const [aiHistory, setAiHistory] =
    useState([]);


  // ============================================================
  // MODALS
  // ============================================================

  const [projectModal, setProjectModal] =
    useState(false);

  const [employeeModal, setEmployeeModal] =
    useState(false);

  const [taskModal, setTaskModal] =
    useState(false);


  const [selectedProject, setSelectedProject] =
    useState(null);


  // ============================================================
  // PROJECT FORM
  // ============================================================

  const [projectForm, setProjectForm] =
    useState({

      name: "",

      description: "",

    });


  // ============================================================
  // EMPLOYEE FORM
  // ============================================================

  const [employeeForm, setEmployeeForm] =
    useState({

      employee_id: "",

    });


  // ============================================================
  // TASK FORM
  // ============================================================

  const [taskForm, setTaskForm] =
    useState({

      project_id: "",

      employee_id: "",

      title: "",

      description: "",

      priority: "Medium",

      due_date: "",

    });


  // ============================================================
  // LOAD ALL MANAGER DATA
  // ============================================================

  const loadDashboard = async () => {

    try {

      setLoading(true);

      setError("");


      const [
        overviewResponse,
        projectsResponse,
        tasksResponse,
        knowledgeResponse,
        activityResponse,
      ] = await Promise.all([


        // ------------------------------------------------------
        // OVERVIEW
        // ------------------------------------------------------

        fetch(
          `${API_BASE}/manager/overview?manager_id=${MANAGER_ID}`
        ),


        // ------------------------------------------------------
        // PROJECTS
        // ------------------------------------------------------

        fetch(
          `${API_BASE}/manager/projects?manager_id=${MANAGER_ID}`
        ),


        // ------------------------------------------------------
        // TASKS
        // ------------------------------------------------------

        fetch(
          `${API_BASE}/manager/tasks?manager_id=${MANAGER_ID}`
        ),


        // ------------------------------------------------------
        // TEAM KNOWLEDGE
        // ------------------------------------------------------

        fetch(
          `${API_BASE}/manager/knowledge?manager_id=${MANAGER_ID}`
        ),


        // ------------------------------------------------------
        // TEAM ACTIVITY
        // ------------------------------------------------------

        fetch(
          `${API_BASE}/manager/activity?manager_id=${MANAGER_ID}`
        ),

      ]);


      if (

        !overviewResponse.ok ||

        !projectsResponse.ok ||

        !tasksResponse.ok ||

        !knowledgeResponse.ok ||

        !activityResponse.ok

      ) {

        throw new Error(
          "Unable to load manager data."
        );

      }


      // ========================================================
      // PARSE RESPONSES
      // ========================================================

      const overviewData =
        await overviewResponse.json();

      const projectsData =
        await projectsResponse.json();

      const tasksData =
        await tasksResponse.json();

      const knowledgeData =
        await knowledgeResponse.json();

      const activityData =
        await activityResponse.json();


      // ========================================================
      // SET STATE
      // ========================================================

      setOverview(
        overviewData
      );

      setProjects(
        projectsData.projects || []
      );

      setTasks(
        tasksData.tasks || []
      );

      setTeamKnowledge(
        knowledgeData.knowledge || []
      );

      setActivities(
        activityData.activities || []
      );


    } catch (err) {

      console.error(
        "Manager Dashboard Error:",
        err
      );

      setError(
        "Unable to connect to the backend. Make sure FastAPI is running."
      );


    } finally {

      setLoading(false);

    }

  };


  // ============================================================
  // INITIAL LOAD
  // ============================================================

  useEffect(() => {

    loadDashboard();

  }, []);


  // ============================================================
  // CREATE PROJECT
  // ============================================================

  const createProject = async (
    event
  ) => {

    event.preventDefault();


    if (
      !projectForm.name.trim()
    ) {

      alert(
        "Please enter project name."
      );

      return;

    }


    try {

      setSubmitting(true);


      const formData =
        new FormData();


      formData.append(
        "name",
        projectForm.name
      );

      formData.append(
        "description",
        projectForm.description
      );

      formData.append(
        "manager_id",
        MANAGER_ID
      );


      const response =
        await fetch(
          `${API_BASE}/manager/projects`,
          {

            method: "POST",

            body: formData,

          }
        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to create project."
        );

      }


      setProjectForm({

        name: "",

        description: "",

      });


      setProjectModal(
        false
      );


      await loadDashboard();


    } catch (err) {

      console.error(err);

      alert(
        err.message
      );


    } finally {

      setSubmitting(false);

    }

  };


  // ============================================================
  // ADD EMPLOYEE
  // ============================================================

  const addEmployee = async (
    event
  ) => {

    event.preventDefault();


    if (
      !selectedProject ||
      !employeeForm.employee_id.trim()
    ) {

      return;

    }


    try {

      setSubmitting(true);


      const formData =
        new FormData();


      formData.append(
        "employee_id",
        employeeForm.employee_id
      );

      formData.append(
        "manager_id",
        MANAGER_ID
      );


      const response =
        await fetch(

          `${API_BASE}/manager/projects/${selectedProject.id}/employees`,

          {

            method: "POST",

            body: formData,

          }

        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to add employee."
        );

      }


      setEmployeeForm({

        employee_id: "",

      });


      setEmployeeModal(
        false
      );


      await loadDashboard();


    } catch (err) {

      console.error(err);

      alert(
        err.message
      );


    } finally {

      setSubmitting(false);

    }

  };


  // ============================================================
  // ASSIGN TASK
  // ============================================================

  const assignTask = async (
    event
  ) => {

    event.preventDefault();


    if (

      !taskForm.project_id ||

      !taskForm.employee_id.trim() ||

      !taskForm.title.trim()

    ) {

      alert(
        "Please fill all required fields."
      );

      return;

    }


    try {

      setSubmitting(true);


      const formData =
        new FormData();


      formData.append(
        "title",
        taskForm.title
      );


      formData.append(
        "description",
        taskForm.description
      );


      formData.append(
        "priority",
        taskForm.priority
      );


      formData.append(
        "employee_id",
        taskForm.employee_id
      );


      formData.append(
        "project_id",
        taskForm.project_id
      );


      formData.append(
        "manager_id",
        MANAGER_ID
      );


      if (
        taskForm.due_date
      ) {

        formData.append(
          "due_date",
          taskForm.due_date
        );

      }


      const response =
        await fetch(

          `${API_BASE}/manager/tasks`,

          {

            method: "POST",

            body: formData,

          }

        );


      const data =
        await response.json();


      if (!response.ok) {

        throw new Error(
          data.detail ||
          "Unable to assign task."
        );

      }


      setTaskForm({

        project_id: "",

        employee_id: "",

        title: "",

        description: "",

        priority: "Medium",

        due_date: "",

      });


      setTaskModal(
        false
      );


      await loadDashboard();


    } catch (err) {

      console.error(err);

      alert(
        err.message
      );


    } finally {

      setSubmitting(false);

    }

  };


  // ============================================================
  // DELETE PROJECT
  // ============================================================

  const deleteProject = async (
    project
  ) => {

    if (!project) {
      return;
    }

    const confirmed = window.confirm(
      `Delete "${project.name}"?\n\nOnly projects with no employees assigned can be deleted.`
    );

    if (!confirmed) {
      return;
    }

    try {

      setSubmitting(true);

      const response =
        await fetch(
          `${API_BASE}/manager/projects/${project.id}?manager_id=${MANAGER_ID}`,
          {
            method: "DELETE",
          }
        );

      const data =
        await response.json();

      if (!response.ok) {

        throw new Error(
          data.detail ||
          data.message ||
          "Unable to delete project."
        );

      }

      alert(
        data.message ||
        "Project deleted successfully."
      );

      await loadDashboard();

    } catch (err) {

      console.error(
        "Delete Project Error:",
        err
      );

      alert(
        err.message ||
        "Unable to delete project."
      );

    } finally {

      setSubmitting(false);

    }

  };


  // ============================================================
  // ASK AI ASSISTANT
  // ============================================================

  const askAI = async (event) => {

    if (event) {
      event.preventDefault();
    }

    const question = aiQuestion.trim();

    if (!question || aiLoading) {
      return;
    }

    try {

      setAiLoading(true);
      setAiError("");
      setAiAnswer("");

      // The existing RAG endpoint is reused here.
      // If your /ask endpoint expects a different payload,
      // only this fetch body needs to be adjusted.
      const response = await fetch(
        `${API_BASE}/ask`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await response.json().catch(() => ({}));

      if (!response.ok) {
        throw new Error(
          data.detail ||
          data.message ||
          "Unable to get an AI response."
        );
      }

      const answer =
        data.answer ||
        data.response ||
        data.result ||
        data.message ||
        "No answer was returned.";

      setAiAnswer(answer);

      setAiHistory((previous) => [
        ...previous,
        {
          question,
          answer,
        },
      ]);

      setAiQuestion("");

    } catch (err) {

      console.error(
        "Manager AI Assistant Error:",
        err
      );

      setAiError(
        err.message ||
        "Unable to connect to the AI Assistant."
      );

    } finally {

      setAiLoading(false);

    }

  };


  // ============================================================
  // OPEN EMPLOYEE MODAL
  // ============================================================

  const openEmployeeModal = (
    project
  ) => {

    setSelectedProject(
      project
    );


    setEmployeeForm({

      employee_id: "",

    });


    setEmployeeModal(
      true
    );

  };


  // ============================================================
  // OPEN TASK MODAL
  // ============================================================

  const openTaskModal = async (
    project = null
  ) => {

    setTaskForm({

      project_id:
        project
          ? String(project.id)
          : "",

      employee_id: "",

      title: "",

      description: "",

      priority: "Medium",

      due_date: "",

    });

    setTaskModal(
      true
    );

    // If the selected project has exactly one employee,
    // automatically fill that employee ID.
    if (project) {

      try {

        const response =
          await fetch(
            `${API_BASE}/manager/projects/${project.id}?manager_id=${MANAGER_ID}`
          );

        if (!response.ok) {
          return;
        }

        const data =
          await response.json();

        const employees =
          data?.project?.employees || [];

        if (employees.length === 1) {

          setTaskForm(
            (previous) => ({
              ...previous,
              project_id: String(project.id),
              employee_id:
                employees[0].employee_id || "",
            })
          );

        }

      } catch (err) {

        console.error(
          "Unable to load project employees:",
          err
        );

      }

    }

  };


  // ============================================================
  // NAVIGATION ITEMS
  // ============================================================

  const navigation = [

    {
      name: "Dashboard",
      icon: LayoutDashboard,
    },

    {
      name: "Projects",
      icon: FolderKanban,
    },

    {
      name: "Team Tasks",
      icon: CheckSquare,
    },

    {
      name: "Team Knowledge",
      icon: Brain,
    },

    {
      name: "AI Assistant",
      icon: Sparkles,
    },

    {
      name: "Activity",
      icon: Activity,
    },

    {
      name: "Settings",
      icon: Settings,
    },

    {
      name: "Help & Support",
      icon: HelpCircle,
    },

  ];


  // ============================================================
  // DASHBOARD PAGE
  // ============================================================

  const DashboardPage = () => (

    <>

      <div className="manager-welcome">

        <div>

          <h1>
            {getGreeting()}, Manager
          </h1>

          <p>
            Here's what's happening with
            your team today.
          </p>

        </div>


        <div className="manager-actions">

          <button
            className="manager-btn manager-btn-secondary"
            onClick={
              loadDashboard
            }
          >

            <RefreshCw size={15} />

            Refresh

          </button>


          <button
            className="manager-btn manager-btn-primary"
            onClick={() =>
              setProjectModal(true)
            }
          >

            <Plus size={15} />

            New Project

          </button>

        </div>

      </div>


      {/* ======================================================
          STATS
      ====================================================== */}

      <div className="manager-stats">


        <div className="manager-stat-card">

          <div className="manager-stat-header">

            <div>

              <span className="manager-stat-title">
                Team Members
              </span>

              <div className="manager-stat-value">
                {overview?.team_members ?? 0}
              </div>

              <div className="manager-stat-description">
                Employees in your projects
              </div>

            </div>

            <div className="manager-stat-icon">
              <Users size={18} />
            </div>

          </div>

        </div>


        <div className="manager-stat-card">

          <div className="manager-stat-header">

            <div>

              <span className="manager-stat-title">
                Projects
              </span>

              <div className="manager-stat-value">
                {overview?.projects ?? 0}
              </div>

              <div className="manager-stat-description">
                Active team projects
              </div>

            </div>

            <div className="manager-stat-icon">
              <FolderKanban size={18} />
            </div>

          </div>

        </div>


        <div className="manager-stat-card">

          <div className="manager-stat-header">

            <div>

              <span className="manager-stat-title">
                Total Tasks
              </span>

              <div className="manager-stat-value">
                {overview?.total_tasks ?? 0}
              </div>

              <div className="manager-stat-description">
                Tasks assigned by you
              </div>

            </div>

            <div className="manager-stat-icon">
              <ClipboardList size={18} />
            </div>

          </div>

        </div>


        <div className="manager-stat-card">

          <div className="manager-stat-header">

            <div>

              <span className="manager-stat-title">
                Team Knowledge
              </span>

              <div className="manager-stat-value">
                {overview?.team_knowledge ?? 0}
              </div>

              <div className="manager-stat-description">
                Safe team knowledge cards
              </div>

            </div>

            <div className="manager-stat-icon">
              <Brain size={18} />
            </div>

          </div>

        </div>


      </div>


      {/* ======================================================
          MIDDLE GRID
      ====================================================== */}

      <div className="manager-middle-grid">


        {/* PROJECTS */}

        <div className="manager-dashboard-card">

          <div className="manager-card-header">

            <div>

              <h3>
                Projects
              </h3>

              <p>
                Your team's active projects
              </p>

            </div>


            <button
              className="manager-view-all"
              onClick={() =>
                setActivePage("Projects")
              }
            >

              View all

              <ArrowUpRight size={13} />

            </button>

          </div>


          <div className="manager-project-list">

            {projects.length === 0 ? (

              <div className="manager-empty">

                <FolderKanban size={30} />

                <strong>
                  No projects yet
                </strong>

                <span>
                  Create your first team project.
                </span>

              </div>

            ) : (

              projects
                .slice(0, 4)
                .map(
                  (project) => (

                    <div
                      className="manager-project-item"
                      key={project.id}
                    >

                      <div className="manager-project-left">

                        <div className="manager-project-icon">
                          <FolderKanban size={17} />
                        </div>

                        <div>

                          <strong>
                            {project.name}
                          </strong>

                          <span>
                            {project.employee_count} employee
                            {project.employee_count !== 1
                              ? "s"
                              : ""}
                          </span>

                        </div>

                      </div>


                      <span className="manager-status">
                        {project.status}
                      </span>

                    </div>

                  )
                )

            )}

          </div>

        </div>


        {/* TASK SUMMARY */}

        <div className="manager-dashboard-card">

          <div className="manager-card-header">

            <div>

              <h3>
                Task Summary
              </h3>

              <p>
                Current team workload
              </p>

            </div>

          </div>


          <div className="manager-summary">


            <div className="manager-summary-item">

              <div>

                <ClipboardList size={17} />

                <span>
                  Total Tasks
                </span>

              </div>

              <strong>
                {overview?.total_tasks ?? 0}
              </strong>

            </div>


            <div className="manager-summary-item">

              <div>

                <Clock3 size={17} />

                <span>
                  Pending
                </span>

              </div>

              <strong>
                {overview?.pending_tasks ?? 0}
              </strong>

            </div>


            <div className="manager-summary-item">

              <div>

                <CheckCircle2 size={17} />

                <span>
                  Completed
                </span>

              </div>

              <strong>
                {overview?.completed_tasks ?? 0}
              </strong>

            </div>


            <button
              className="manager-full-button"
              onClick={() =>
                setActivePage("Team Tasks")
              }
            >

              View Team Tasks

            </button>


          </div>

        </div>

      </div>


      {/* ======================================================
          RECENT ACTIVITY
      ====================================================== */}

      <div className="manager-dashboard-card manager-recent-card">

        <div className="manager-card-header">

          <div>

            <h3>
              Recent Team Activity
            </h3>

            <p>
              Latest tasks and team actions
            </p>

          </div>

          <Activity size={19} />

        </div>


        <div className="manager-task-list">

          {activities.length === 0 ? (

            <div className="manager-empty">

              <Activity size={30} />

              <strong>
                No recent activity
              </strong>

            </div>

          ) : (

            activities
              .slice(0, 5)
              .map(
                (item, index) => (

                  <div
                    className="manager-task-item"
                    key={`${item.type}-${index}`}
                  >

                    <div className="manager-task-left">

                      <div className="manager-task-icon">

                        {item.type === "knowledge"
                          ? <Brain size={17} />
                          : item.type === "employee"
                            ? <UserPlus size={17} />
                            : item.type === "project"
                              ? <FolderKanban size={17} />
                              : <CheckSquare size={17} />
                        }

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


                    <div className="manager-task-right">

                      <small>

                        {item.timestamp
                          ? new Date(
                              item.timestamp
                            ).toLocaleDateString()
                          : ""}

                      </small>

                    </div>

                  </div>

                )
              )

          )}

        </div>

      </div>

    </>

  );


  // ============================================================
  // PROJECTS PAGE
  // ============================================================

  const ProjectsPage = () => (

    <>

      <div className="manager-page-header">

        <div>

          <h1>
            Projects
          </h1>

          <p>
            Manage your team's projects
            and employees.
          </p>

        </div>


        <button
          className="manager-btn manager-btn-primary"
          onClick={() =>
            setProjectModal(true)
          }
        >

          <Plus size={15} />

          Create Project

        </button>

      </div>


      <div className="manager-project-grid">

        {projects.length === 0 ? (

          <div className="manager-dashboard-card">

            <div className="manager-empty">

              <FolderKanban size={30} />

              <strong>
                No projects yet
              </strong>

            </div>

          </div>

        ) : (

          projects.map(
            (project) => (

              <div
                className="manager-project-card"
                key={project.id}
              >

                <div className="manager-project-card-top">

                  <div className="manager-project-large-icon">

                    <FolderKanban size={20} />

                  </div>


                  <span className="manager-status">
                    {project.status}
                  </span>

                </div>


                <h3>
                  {project.name}
                </h3>


                <p>
                  {project.description ||
                    "No description provided."}
                </p>


                <div className="manager-project-count">

                  <Users size={16} />

                  {project.employee_count} employee
                  {project.employee_count !== 1
                    ? "s"
                    : ""}

                </div>


                <div className="manager-project-actions">

                  <button
                    className="manager-btn manager-btn-secondary"
                    onClick={() =>
                      openEmployeeModal(project)
                    }
                  >

                    <UserPlus size={14} />

                    Add Employee

                  </button>


                  <button
                    className="manager-btn manager-btn-primary"
                    onClick={() =>
                      openTaskModal(project)
                    }
                  >

                    <Plus size={14} />

                    Assign Task

                  </button>


                  <button
                    className="manager-btn manager-btn-danger"
                    onClick={() =>
                      deleteProject(project)
                    }
                    disabled={submitting}
                    title={
                      project.employee_count > 0
                        ? "Remove employees before deleting this project."
                        : "Delete project"
                    }
                  >

                    <Trash2 size={14} />

                    Delete

                  </button>

                </div>

              </div>

            )
          )

        )}

      </div>

    </>

  );


  // ============================================================
  // TEAM TASKS PAGE
  // ============================================================

  const TeamTasksPage = () => (

    <>

      <div className="manager-page-header">

        <div>

          <h1>
            Team Tasks
          </h1>

          <p>
            Monitor tasks assigned to
            your team.
          </p>

        </div>


        <button
          className="manager-btn manager-btn-primary"
          onClick={() =>
            openTaskModal()
          }
        >

          <Plus size={15} />

          Assign Task

        </button>

      </div>


      <div className="manager-table-wrapper">

        {tasks.length === 0 ? (

          <div className="manager-empty">

            <CheckSquare size={30} />

            <strong>
              No team tasks
            </strong>

            <span>
              Tasks assigned to your team
              will appear here.
            </span>

          </div>

        ) : (

          <table className="manager-table">

            <thead>

              <tr>

                <th>
                  Task
                </th>

                <th>
                  Employee
                </th>

                <th>
                  Priority
                </th>

                <th>
                  Status
                </th>

                <th>
                  Due Date
                </th>

              </tr>

            </thead>


            <tbody>

              {tasks.map(
                (task) => (

                  <tr key={task.id}>

                    <td>

                      <strong>
                        {task.title}
                      </strong>

                      <span className="table-description">
                        {task.description ||
                          "No description"}
                      </span>

                    </td>


                    <td>
                      {task.employee_id}
                    </td>


                    <td>

                      <span className="manager-priority">
                        {task.priority}
                      </span>

                    </td>


                    <td>

                      <span className="manager-status">
                        {task.status}
                      </span>

                    </td>


                    <td>

                      {task.due_date
                        ? new Date(
                            task.due_date
                          ).toLocaleString()
                        : "No due date"}

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        )}

      </div>

    </>

  );


  // ============================================================
  // TEAM KNOWLEDGE PAGE
  // ============================================================

  const TeamKnowledgePage = () => (

    <>

      <div className="manager-page-header">

        <div>

          <h1>
            Team Knowledge
          </h1>

          <p>
            Safe knowledge shared by
            employees in your projects.
          </p>

        </div>


        <div className="manager-knowledge-count">

          <Brain size={16} />

          {teamKnowledge.length}
          {" "}
          knowledge cards

        </div>

      </div>


      {teamKnowledge.length === 0 ? (

        <div className="manager-dashboard-card">

          <div className="manager-empty manager-knowledge-empty">

            <Brain size={32} />

            <strong>
              No team knowledge available
            </strong>

            <span>
              Knowledge uploaded by your
              team will appear here.
            </span>

          </div>

        </div>

      ) : (

        <div className="manager-knowledge-grid">

          {teamKnowledge.map(
            (knowledge) => (

              <div
                className="manager-knowledge-card"
                key={knowledge.id}
              >

                <div className="manager-knowledge-top">

                  <div className="manager-knowledge-icon">

                    <Brain size={18} />

                  </div>


                  <span className="manager-knowledge-category">

                    {knowledge.category}

                  </span>

                </div>


                <h3>
                  {knowledge.title}
                </h3>


                <p>
                  {knowledge.summary}
                </p>


                <div className="manager-knowledge-footer">

                  <span>

                    Confidence:{" "}

                    {Math.round(
                      knowledge.confidence * 100
                    )}

                    %

                  </span>


                  <span>

                    {knowledge.timestamp
                      ? new Date(
                          knowledge.timestamp
                        ).toLocaleDateString()
                      : ""}

                  </span>

                </div>

              </div>

            )
          )}

        </div>

      )}

    </>

  );


  // ============================================================
  // TEAM ACTIVITY PAGE
  // ============================================================

  const TeamActivityPage = () => (

    <>

      <div className="manager-page-header">

        <div>

          <h1>
            Team Activity
          </h1>

          <p>
            Monitor recent work and changes
            across your team.
          </p>

        </div>


        <button
          className="manager-btn manager-btn-secondary"
          onClick={
            loadDashboard
          }
        >

          <RefreshCw size={15} />

          Refresh

        </button>

      </div>


      <div className="manager-activity-card">

        {activities.length === 0 ? (

          <div className="manager-empty">

            <Activity size={32} />

            <strong>
              No team activity yet
            </strong>

            <span>
              Recent team actions will
              appear here.
            </span>

          </div>

        ) : (

          <div className="manager-activity-list">

            {activities.map(
              (item, index) => (

                <div
                  className="manager-activity-item"
                  key={`${item.type}-${index}`}
                >

                  <div
                    className={`manager-activity-icon ${item.type}`}
                  >

                    {item.type === "task"
                      ? <CheckSquare size={17} />
                      : item.type === "knowledge"
                        ? <Brain size={17} />
                        : item.type === "employee"
                          ? <UserPlus size={17} />
                          : <FolderKanban size={17} />
                    }

                  </div>


                  <div className="manager-activity-content">

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
                          ).toLocaleString()
                        : "Recent"}

                    </small>

                  </div>

                </div>

              )
            )}

          </div>

        )}

      </div>

    </>

  );


  // ============================================================
  // AI ASSISTANT PAGE
  // ============================================================

  const AIAssistantPage = () => (

    <>

      <div className="manager-page-header">

        <div>

          <div className="manager-ai-page-title">

            <div className="manager-ai-page-icon">
              <Sparkles size={19} />
            </div>

            <div>

              <h1>
                AI Assistant
              </h1>

              <p>
                Ask questions about your team's projects,
                tasks and available knowledge.
              </p>

            </div>

          </div>

        </div>

      </div>


      <div className="manager-ai-assistant-card">

        <div className="manager-ai-assistant-header">

          <div className="manager-ai-assistant-avatar">
            <Sparkles size={21} />
          </div>

          <div>

            <h3>
              Manager AI
            </h3>

            <p>
              Powered by the existing RAG / Ask pipeline
            </p>

          </div>

          <span className="manager-ai-online">
            AI Ready
          </span>

        </div>


        <div className="manager-ai-suggestions">

          <button
            type="button"
            onClick={() =>
              setAiQuestion(
                "What projects are currently active?"
              )
            }
          >
            <FolderKanban size={15} />
            Active projects
          </button>

          <button
            type="button"
            onClick={() =>
              setAiQuestion(
                "What tasks are currently pending?"
              )
            }
          >
            <CheckSquare size={15} />
            Pending tasks
          </button>

          <button
            type="button"
            onClick={() =>
              setAiQuestion(
                "What knowledge is available for my team?"
              )
            }
          >
            <Brain size={15} />
            Team knowledge
          </button>

        </div>


        <div className="manager-ai-conversation">

          {aiHistory.length === 0 && !aiAnswer && !aiLoading && (

            <div className="manager-ai-empty">

              <div className="manager-ai-empty-icon">
                <MessageCircle size={25} />
              </div>

              <h3>
                How can I help?
              </h3>

              <p>
                Ask a question about your team's
                projects, tasks or knowledge.
              </p>

            </div>

          )}


          {aiHistory.map(
            (item, index) => (

              <div
                className="manager-ai-history"
                key={`${index}-${item.question}`}
              >

                <div className="manager-ai-question">

                  <span>
                    You
                  </span>

                  <p>
                    {item.question}
                  </p>

                </div>


                <div className="manager-ai-answer">

                  <div className="manager-ai-answer-label">

                    <Sparkles size={14} />

                    AI Assistant

                  </div>

                  <p>
                    {item.answer}
                  </p>

                </div>

              </div>

            )
          )}


          {aiLoading && (

            <div className="manager-ai-loading">

              <Sparkles
                size={17}
                className="manager-spin"
              />

              <span>
                Searching team knowledge and generating an answer...
              </span>

            </div>

          )}

        </div>


        {aiError && (

          <div className="manager-ai-error">

            {aiError}

          </div>

        )}


        <form
          className="manager-ai-input-area"
          onSubmit={askAI}
        >

          <textarea
            value={aiQuestion}
            onChange={(event) =>
              setAiQuestion(
                event.target.value
              )
            }
            placeholder="Ask your team something..."
            rows={2}
            disabled={aiLoading}
          />

          <button
            type="submit"
            className="manager-ai-send"
            disabled={
              aiLoading ||
              !aiQuestion.trim()
            }
          >

            <Send size={17} />

            {aiLoading
              ? "Thinking..."
              : "Ask AI"}

          </button>

        </form>

      </div>

    </>

  );


  // ============================================================
  // PLACEHOLDER PAGE
  // ============================================================

  const PlaceholderPage = ({
    title,
    icon: Icon,
    description,
  }) => (

    <div className="manager-placeholder">

      <div className="manager-placeholder-icon">

        <Icon size={27} />

      </div>


      <h1>
        {title}
      </h1>


      <p>

        {description ||
          "This Manager section will be connected next."}

      </p>

    </div>

  );


  // ============================================================
  // PAGE RENDERER
  // ============================================================

  const renderPage = () => {

    if (
      activePage === "Projects"
    ) {

      return <ProjectsPage />;

    }


    if (
      activePage === "Team Tasks"
    ) {

      return <TeamTasksPage />;

    }


    if (
      activePage === "Team Knowledge"
    ) {

      return <TeamKnowledgePage />;

    }


    if (
      activePage === "Activity"
    ) {

      return <TeamActivityPage />;

    }


    if (
      activePage === "AI Assistant"
    ) {

      return <AIAssistantPage />;

    }


    if (
      activePage === "Settings"
    ) {

      return (

        <PlaceholderPage
          title="Manager Settings"
          icon={Settings}
          description="Manager settings will be connected here."
        />

      );

    }


    if (
      activePage ===
      "Help & Support"
    ) {

      return (

        <PlaceholderPage
          title="Help & Support"
          icon={HelpCircle}
          description="Manager help and support options will be connected here."
        />

      );

    }


    return <DashboardPage />;

  };


  // ============================================================
  // MAIN RETURN
  // ============================================================

  return (

    <div className="manager-dashboard">


      {/* ======================================================
          SIDEBAR
      ====================================================== */}

      <aside className="manager-sidebar">


        <div className="manager-brand">

          <div className="manager-brand-icon">
            AI
          </div>


          <div>

            <h2>
              RABC System
            </h2>

            <span>
              Manager Workspace
            </span>

          </div>

        </div>


        <nav className="manager-navigation">

          {navigation.map(
            (item) => {

              const Icon =
                item.icon;


              return (

                <button
                  key={item.name}
                  className={`manager-nav-item ${
                    activePage === item.name
                      ? "active"
                      : ""
                  }`}
                  onClick={() =>
                    setActivePage(
                      item.name
                    )
                  }
                >

                  <Icon size={18} />

                  <span>
                    {item.name}
                  </span>

                </button>

              );

            }
          )}

        </nav>


        <div className="manager-sidebar-ai">

          <div>

            <Brain size={16} />

            Manager AI

          </div>


          <p>

            Get insights about your
            team's work, projects
            and activity.

          </p>


          <button
            onClick={() =>
              setActivePage(
                "AI Assistant"
              )
            }
          >

            Open AI Assistant

            <ArrowUpRight
              size={13}
            />

          </button>

        </div>


        <div className="manager-profile">

          <div className="manager-avatar">
            M
          </div>


          <div>

            <strong>
              Manager
            </strong>

            <span>
              {MANAGER_ID}
            </span>

          </div>

        </div>


      </aside>


      {/* ======================================================
          MAIN
      ====================================================== */}

      <main className="manager-main">


        <header className="manager-topbar">


          <div className="manager-search">

            <Search size={17} />

            <input
              placeholder="Search..."
            />

          </div>


          <div className="manager-top-actions">


            <button className="manager-notification">

              <Bell size={19} />

              <span />

            </button>


            <div className="manager-profile">

              <div className="manager-avatar">
                M
              </div>


              <div>

                <strong>
                  Manager
                </strong>

                <span>
                  {MANAGER_ID}
                </span>

              </div>

            </div>


          </div>


        </header>


        <div className="manager-content">


          {error && (

            <div className="manager-error">

              <span>
                {error}
              </span>


              <button
                onClick={
                  loadDashboard
                }
              >
                Retry
              </button>

            </div>

          )}


          {loading ? (

            <div className="manager-loading">

              <RefreshCw
                size={27}
                className="manager-spin"
              />

              <span>
                Loading manager dashboard...
              </span>

            </div>

          ) : (

            renderPage()

          )}


        </div>


      </main>


      {/* ======================================================
          CREATE PROJECT MODAL
      ====================================================== */}

      {projectModal && (

        <div className="manager-modal-overlay">

          <div className="manager-modal">


            <div className="manager-modal-header">

              <div>

                <h2>
                  Create Project
                </h2>

                <p>
                  Create a new team project.
                </p>

              </div>


              <button
                className="manager-close"
                onClick={() =>
                  setProjectModal(
                    false
                  )
                }
              >

                <X size={18} />

              </button>

            </div>


            <form
              className="manager-modal-body"
              onSubmit={
                createProject
              }
            >

              <label>

                Project Name

                <input
                  value={
                    projectForm.name
                  }
                  onChange={(event) =>
                    setProjectForm({

                      ...projectForm,

                      name:
                        event.target.value,

                    })
                  }
                  placeholder="AI Loss Prevention"
                  required
                />

              </label>


              <label>

                Description

                <textarea
                  value={
                    projectForm.description
                  }
                  onChange={(event) =>
                    setProjectForm({

                      ...projectForm,

                      description:
                        event.target.value,

                    })
                  }
                  placeholder="Project description..."
                />

              </label>


              <button
                className="manager-modal-submit"
                disabled={
                  submitting
                }
              >

                {submitting
                  ? "Creating..."
                  : "Create Project"}

              </button>


            </form>

          </div>

        </div>

      )}


      {/* ======================================================
          ADD EMPLOYEE MODAL
      ====================================================== */}

      {employeeModal && (

        <div className="manager-modal-overlay">

          <div className="manager-modal">


            <div className="manager-modal-header">

              <div>

                <h2>
                  Add Employee
                </h2>

                <p>
                  Add an employee to{" "}
                  {selectedProject?.name}.
                </p>

              </div>


              <button
                className="manager-close"
                onClick={() =>
                  setEmployeeModal(
                    false
                  )
                }
              >

                <X size={18} />

              </button>

            </div>


            <form
              className="manager-modal-body"
              onSubmit={
                addEmployee
              }
            >

              <label>

                Employee ID

                <input
                  value={
                    employeeForm.employee_id
                  }
                  onChange={(event) =>
                    setEmployeeForm({

                      employee_id:
                        event.target.value,

                    })
                  }
                  placeholder="EMP001"
                  required
                />

              </label>


              <button
                className="manager-modal-submit"
                disabled={
                  submitting
                }
              >

                {submitting
                  ? "Adding..."
                  : "Add Employee"}

              </button>


            </form>

          </div>

        </div>

      )}


      {/* ======================================================
          ASSIGN TASK MODAL
      ====================================================== */}

      {taskModal && (

        <div className="manager-modal-overlay">

          <div className="manager-modal">


            <div className="manager-modal-header">

              <div>

                <h2>
                  Assign Task
                </h2>

                <p>
                  Assign work to a project employee.
                </p>

              </div>


              <button
                className="manager-close"
                onClick={() =>
                  setTaskModal(
                    false
                  )
                }
              >

                <X size={18} />

              </button>

            </div>


            <form
              className="manager-modal-body"
              onSubmit={
                assignTask
              }
            >


              <label>

                Project

                <select
                  value={
                    taskForm.project_id
                  }
                  onChange={async (event) => {

                    const projectId =
                      event.target.value;

                    setTaskForm({

                      ...taskForm,

                      project_id:
                        projectId,

                      employee_id:
                        "",

                    });

                    if (!projectId) {
                      return;
                    }

                    try {

                      const response =
                        await fetch(
                          `${API_BASE}/manager/projects/${projectId}?manager_id=${MANAGER_ID}`
                        );

                      if (!response.ok) {
                        return;
                      }

                      const data =
                        await response.json();

                      const employees =
                        data?.project?.employees || [];

                      if (employees.length === 1) {

                        setTaskForm(
                          (previous) => ({
                            ...previous,
                            project_id:
                              projectId,
                            employee_id:
                              employees[0].employee_id || "",
                          })
                        );

                      }

                    } catch (err) {

                      console.error(
                        "Unable to load project employees:",
                        err
                      );

                    }

                  }}
                  required
                >

                  <option value="">
                    Select Project
                  </option>


                  {projects.map(
                    (project) => (

                      <option
                        key={project.id}
                        value={project.id}
                      >

                        {project.name}

                      </option>

                    )
                  )}

                </select>

              </label>


              <label>

                Employee ID

                <input
                  value={
                    taskForm.employee_id
                  }
                  onChange={(event) =>
                    setTaskForm({

                      ...taskForm,

                      employee_id:
                        event.target.value,

                    })
                  }
                  placeholder="EMP001"
                  required
                />

                {taskForm.employee_id && (
                  <small className="manager-form-hint">
                    Employee automatically selected from this project.
                  </small>
                )}

              </label>


              <label>

                Task Title

                <input
                  value={
                    taskForm.title
                  }
                  onChange={(event) =>
                    setTaskForm({

                      ...taskForm,

                      title:
                        event.target.value,

                    })
                  }
                  placeholder="Complete RAG evaluation"
                  required
                />

              </label>


              <label>

                Description

                <textarea
                  value={
                    taskForm.description
                  }
                  onChange={(event) =>
                    setTaskForm({

                      ...taskForm,

                      description:
                        event.target.value,

                    })
                  }
                  placeholder="Describe the task..."
                />

              </label>


              <div className="manager-form-row">


                <label>

                  Priority

                  <select
                    value={
                      taskForm.priority
                    }
                    onChange={(event) =>
                      setTaskForm({

                        ...taskForm,

                        priority:
                          event.target.value,

                      })
                    }
                  >

                    <option>
                      Low
                    </option>

                    <option>
                      Medium
                    </option>

                    <option>
                      High
                    </option>

                  </select>

                </label>


                <label>

                  Due Date

                  <input
                    type="datetime-local"
                    value={
                      taskForm.due_date
                    }
                    onChange={(event) =>
                      setTaskForm({

                        ...taskForm,

                        due_date:
                          event.target.value,

                      })
                    }
                  />

                </label>


              </div>


              <button
                className="manager-modal-submit"
                disabled={
                  submitting
                }
              >

                {submitting
                  ? "Assigning..."
                  : "Assign Task"}

              </button>


            </form>

          </div>

        </div>

      )}

    </div>

  );

}


export default ManagerDashboard;