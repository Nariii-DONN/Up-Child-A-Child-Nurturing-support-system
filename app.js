
import React, { useState, useEffect } from 'react';
import './App.css';

// API Configuration - Using your Render URL for production
const API_BASE_URL = "https://upchild-api.onrender.com";

export default function App() {
  // ========== GENERAL STATES ==========
  const [view, setView] = useState("welcome");
  const [userType, setUserType] = useState("parent");
  const [auth, setAuth] = useState({ token: null, user: null, parentName: null, role: null, teamMemberId: null });
  const [msg, setMsg] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  // ========== PARENT LOGIN/REGISTER STATES ==========
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [parentName, setParentName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  // ========== TEAM MEMBER LOGIN/REGISTER STATES ==========
  const [teamUsername, setTeamUsername] = useState("");
  const [teamEmail, setTeamEmail] = useState("");
  const [teamPassword, setTeamPassword] = useState("");
  const [teamFullName, setTeamFullName] = useState("");
  const [teamRole, setTeamRole] = useState("volunteer");

  // ========== PARENT DASHBOARD STATES ==========
  const [childName, setChildName] = useState("");
  const [childBirthDate, setChildBirthDate] = useState("");
  const [childGender, setChildGender] = useState("");
  const [children, setChildren] = useState([]);
  const [selectedChild, setSelectedChild] = useState(null);
  const [childDetails, setChildDetails] = useState(null);
  const [recordDate, setRecordDate] = useState("");
  const [height, setHeight] = useState("");
  const [weight, setWeight] = useState("");
  const [notes, setNotes] = useState("");
  const [activeTab, setActiveTab] = useState("health");
  const [currentGame, setCurrentGame] = useState(null);
  const [requestType, setRequestType] = useState("");
  const [requestAmount, setRequestAmount] = useState("");
  const [requestReason, setRequestReason] = useState("");
  const [requests, setRequests] = useState([]);
  const [showHelpSection, setShowHelpSection] = useState(false);
  const [showChatbot, setShowChatbot] = useState(false);
  const [showGoalForm, setShowGoalForm] = useState(false);
  const [goalDescription, setGoalDescription] = useState("");
  const [goalTargetDate, setGoalTargetDate] = useState("");
  const [chatMessages, setChatMessages] = useState([
    { id: 1, type: "bot", text: "Hi! 👋 I'm UpChild Assistant. How can I help you today?" }
  ]);
  const [chatInput, setChatInput] = useState("");

  // ========== GAMES STATES ==========
  const [colorScore, setColorScore] = useState(0);
  const [colorTargetIdx, setColorTargetIdx] = useState(0);
  const [colorTime, setColorTime] = useState(60);
  const colorOptions = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F'];
  const [numSequence, setNumSequence] = useState([]);
  const [numClicked, setNumClicked] = useState([]);
  const [reactionScore, setReactionScore] = useState(0);
  const [reactionColor, setReactionColor] = useState('#667eea');
  const [reactionReady, setReactionReady] = useState(false);
  const [reactionStartTime, setReactionStartTime] = useState(null);

  // ========== TEAM MEMBER DASHBOARD STATES ==========
  const [inventory, setInventory] = useState([]);
  const [funds, setFunds] = useState({ total_available: 0, total_allocated: 0, total_distributed: 0 });
  const [fundAllocations, setFundAllocations] = useState([]);
  const [distributionHistory, setDistributionHistory] = useState([]);
  const [teamMembers, setTeamMembers] = useState([]);
  const [teamActiveTab, setTeamActiveTab] = useState("cases");

  // ========== INVENTORY FORM STATES ==========
  const [newItemName, setNewItemName] = useState("");
  const [newItemType, setNewItemType] = useState("");
  const [newItemQty, setNewItemQty] = useState("");
  const [newItemUnit, setNewItemUnit] = useState("pcs");
  const [newItemDesc, setNewItemDesc] = useState("");

  // ========== DISTRIBUTION FORM STATES ==========
  const [distribInventoryId, setDistribInventoryId] = useState("");
  const [distribQty, setDistribQty] = useState("");
  const [distribTo, setDistribTo] = useState("");
  const [distribNotes, setDistribNotes] = useState("");

  // ========== FUND FORM STATES ==========
  const [addFundAmount, setAddFundAmount] = useState("");
  const [allocFundParentId, setAllocFundParentId] = useState("");
  const [allocFundAmount, setAllocFundAmount] = useState("");
  const [allocFundNotes, setAllocFundNotes] = useState("");

  // ========== CASE REPORTING STATES (NEW) ==========
  const [cases, setCases] = useState([]);
  const [selectedCase, setSelectedCase] = useState(null);
  const [showCaseForm, setShowCaseForm] = useState(false);
  const [casePhoto, setCasePhoto] = useState("");
  const [caseLatitude, setCaseLatitude] = useState("");
  const [caseLongitude, setCaseLongitude] = useState("");
  const [caseLocation, setCaseLocation] = useState("");
  const [casePriority, setCasePriority] = useState("Medium");
  const [caseDescription, setCaseDescription] = useState("");
  const [caseCategory, setCaseCategory] = useState("Child");
  const [caseChildName, setCaseChildName] = useState("");
  const [caseChildAge, setCaseChildAge] = useState("");

  const healthResources = [
    {
      type: "Doctor",
      icon: "🏥",
      description: "Medical professionals for health consultations",
      services: ["General Checkup", "Vaccination", "Emergency Care"],
      contact: "Call: 1-800-DOCTOR-1",
      email: "doctors@healthhelp.com"
    },
    {
      type: "Social Worker",
      icon: "👤",
      description: "Support for family and social issues",
      services: ["Family Counseling", "School Issues", "Financial Guidance"],
      contact: "Call: 1-800-SOCIAL-1",
      email: "support@socialcare.com"
    },
    {
      type: "NGO",
      icon: "🤝",
      description: "Non-profit organizations for child welfare",
      services: ["Food & Nutrition", "Education Support", "Crisis Help"],
      contact: "Call: 1-800-NGO-HELP",
      email: "ngo@childcare.com"
    }
  ];

  const chatbotResponses = {
    "parenting": "Great question! Here are some parenting tips:\n• Be consistent with rules\n• Listen actively to your child\n• Praise good behavior\n• Set realistic expectations\nWould you like more specific advice?",
    "health": "Health is important! 💪\n• Regular check-ups\n• Balanced nutrition\n• Exercise daily\n• Good sleep (8-10 hours for kids)\nDo you have specific health concerns?",
    "behavior": "Behavior management tips:\n• Identify triggers\n• Stay calm\n• Use positive reinforcement\n• Set clear boundaries\n• Reward good behavior\nWhat specific behavior concerns you?",
    "game": "Our games help develop:\n🎨 Color Match - Visual perception\n🔢 Sequence - Logic & Memory\n⚡ Reaction - Speed & Focus\nPlaying 15-20 minutes daily is ideal!",
    "sleep": "Sleep Tips for Children:\n• Consistent bedtime\n• Dark, quiet room\n• No screens 1 hour before bed\n• Relaxing routine\n• Age 5-12: 9-11 hours\nNeed help with sleep issues?",
    "nutrition": "Healthy nutrition for kids:\n• 5 servings of fruits/vegetables\n• Whole grains\n• Lean proteins\n• Calcium-rich foods\n• Limit sugar & processed food\nAny dietary concerns?",
    "vaccine": "Vaccination is crucial! 💉\n• Protects from diseases\n• Follow schedule from health worker\n• Common vaccines: DPT, MMR, Polio\n• Consult doctor for timing\nNeed vaccine schedule info?",
    "stress": "Parenting can be stressful. Remember:\n• You're doing great!\n• Take breaks\n• Connect with other parents\n• Practice self-care\n• Seek professional help if needed\nWould you like support resources?",
    "default": "I can help with:\n✓ Parenting tips\n✓ Child health & nutrition\n✓ Behavior management\n✓ Game coaching\n✓ Developmental milestones\n✓ Stress management\n\nWhat would you like help with?"
  };

  // ========== CHATBOT HANDLER ==========
  const handleChatSend = () => {
    if (!chatInput.trim()) return;

    const userMsg = { id: Date.now(), type: "user", text: chatInput };
    setChatMessages([...chatMessages, userMsg]);

    let response = chatbotResponses.default;
    const input = chatInput.toLowerCase();

    if (input.includes("parenting") || input.includes("parent")) response = chatbotResponses.parenting;
    else if (input.includes("health") || input.includes("sick")) response = chatbotResponses.health;
    else if (input.includes("behavior") || input.includes("mood")) response = chatbotResponses.behavior;
    else if (input.includes("game") || input.includes("play")) response = chatbotResponses.game;
    else if (input.includes("sleep") || input.includes("bed")) response = chatbotResponses.sleep;
    else if (input.includes("nutrition") || input.includes("food") || input.includes("eat")) response = chatbotResponses.nutrition;
    else if (input.includes("vaccine")) response = chatbotResponses.vaccine;
    else if (input.includes("stress") || input.includes("worry")) response = chatbotResponses.stress;

    setTimeout(() => {
      const botMsg = { id: Date.now() + 1, type: "bot", text: response };
      setChatMessages(prev => [...prev, botMsg]);
    }, 500);

    setChatInput("");
  };

  // ========== PARENT AUTHENTICATION ==========

  const register = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!parentName || !email || !password || !confirmPassword) {
      setMsg("All fields required");
      setIsLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setMsg("Passwords don't match");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: parentName, email, password })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("Registration successful! Redirecting to login...");
        setParentName("");
        setEmail("");
        setPassword("");
        setConfirmPassword("");
        setTimeout(() => setView("login"), 2000);
      } else {
        setMsg("Error: " + (data.error || "Registration failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const login = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!email || !password) {
      setMsg("Email and password required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      const data = await response.json();

      if (response.ok) {
        setAuth({ token: data.token, user: email, parentName: data.parentName, role: "parent" });
        setView("dashboard");
        setEmail("");
        setPassword("");
        setMsg("Login successful!");
      } else {
        setMsg("Error: " + (data.error || "Login failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  // ========== TEAM MEMBER AUTHENTICATION ==========

  const teamRegister = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!teamUsername || !teamEmail || !teamPassword || !teamFullName) {
      setMsg("All fields required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/team/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: teamUsername,
          email: teamEmail,
          password: teamPassword,
          full_name: teamFullName,
          role: teamRole
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("Team member registered! Redirecting to login...");
        setTeamUsername("");
        setTeamEmail("");
        setTeamPassword("");
        setTeamFullName("");
        setTimeout(() => { setView("team-login"); setUserType("team"); }, 2000);
      } else {
        setMsg("Error: " + (data.error || "Registration failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const teamLogin = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!teamEmail || !teamPassword) {
      setMsg("Email and password required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/team/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: teamEmail, password: teamPassword })
      });
      const data = await response.json();

      if (response.ok) {
        setAuth({
          token: data.token,
          user: teamEmail,
          parentName: data.full_name,
          role: data.role,
          teamMemberId: data.team_member_id
        });
        setView("team-dashboard");
        setUserType("team");
        setTeamEmail("");
        setTeamPassword("");
        setMsg("Login successful!");
        await fetchTeamData(data.token);
      } else {
        setMsg("Error: " + (data.error || "Login failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  // ========== PARENT FUNCTIONS ==========

  useEffect(() => {
    if (auth.token && view === "dashboard" && userType === "parent") {
      fetchChildren();
    }
  }, [auth.token, view]);

  useEffect(() => {
    if (currentGame === "color" && colorTime > 0) {
      const timer = setTimeout(() => setColorTime(colorTime - 1), 1000);
      return () => clearTimeout(timer);
    } else if (currentGame === "color" && colorTime === 0) {
      setMsg("Time's up! Final Score: " + colorScore);
      setCurrentGame(null);
    }
  }, [colorTime, currentGame]);

  const fetchChildren = async () => {
    if (!auth.token) return;
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/children`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        }
      });
      const data = await response.json();
      if (response.ok) {
        setChildren(data);
        setMsg("");
      } else {
        setMsg("Error: " + (data.error || "Failed to fetch children"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const fetchChildDetails = async (childId) => {
    if (!auth.token) return;
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/child/${childId}`, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        }
      });
      const data = await response.json();
      if (response.ok) {
        setChildDetails(data);
        setSelectedChild(childId);
        setView("child-details");
        setActiveTab("health");
      } else {
        setMsg(data.error || "Failed to fetch details");
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const addChild = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!childName || !childBirthDate || !childGender) {
      setMsg("All fields required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/add_child`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          name: childName,
          birth_date: childBirthDate,
          gender: childGender
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("Child added successfully!");
        setChildName("");
        setChildBirthDate("");
        setChildGender("");
        await fetchChildren();
        setTimeout(() => setView("dashboard"), 1000);
      } else {
        setMsg("Error: " + (data.error || "Failed to add child"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const addHealthRecord = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!recordDate || !height || !weight) {
      setMsg("Date, height, and weight required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/child/${selectedChild}/health`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          record_date: recordDate,
          height_cm: parseFloat(height),
          weight_kg: parseFloat(weight),
          notes: notes
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("Health record added!");
        setRecordDate("");
        setHeight("");
        setWeight("");
        setNotes("");
        fetchChildDetails(selectedChild);
      } else {
        setMsg("Error: " + (data.error || "Failed to add record"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const calculateBMI = (weight, height) => {
    if (!weight || !height) return 0;
    return (weight / ((height / 100) ** 2)).toFixed(2);
  };

  const getBMICategory = (bmi) => {
    if (bmi < 18.5) return "Underweight";
    if (bmi < 25) return "Normal";
    if (bmi < 30) return "Overweight";
    return "Obese";
  };

  // ========== GOALS FUNCTIONS ==========
  const addGoal = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!goalDescription || !goalTargetDate) {
      setMsg("Goal description and target date required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/child/${selectedChild}/goals`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          description: goalDescription,
          target_date: goalTargetDate
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Goal added successfully!");
        setGoalDescription("");
        setGoalTargetDate("");
        setShowGoalForm(false);
        fetchChildDetails(selectedChild);
      } else {
        setMsg("Error: " + (data.error || "Failed to add goal"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const toggleGoalCompletion = async (goalId) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/child/${selectedChild}/goals/${goalId}`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          status: "toggle"
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Goal status updated!");
        fetchChildDetails(selectedChild);
      } else {
        setMsg("Error: " + (data.error || "Failed to update goal"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const deleteGoal = async (goalId) => {
    if (!window.confirm("Are you sure you want to delete this goal?")) return;
    
    setIsLoading(true);
    try {
      const response = await fetch(`${API_BASE_URL}/child/${selectedChild}/goals/${goalId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${auth.token}`
        }
      });

      if (response.ok) {
        setMsg("✅ Goal deleted!");
        fetchChildDetails(selectedChild);
      } else {
        setMsg("Error: Failed to delete goal");
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  // ========== GAMES FUNCTIONS ==========

  const startColorMatch = () => {
    setColorScore(0);
    setColorTargetIdx(Math.floor(Math.random() * colorOptions.length));
    setColorTime(60);
    setCurrentGame("color");
    setMsg("Match the colors! Click the same color as shown");
  };

  const handleColorClick = (index) => {
    if (index === colorTargetIdx) {
      setColorScore(colorScore + 10);
      setColorTargetIdx(Math.floor(Math.random() * colorOptions.length));
    } else {
      if (colorTime > 0) setColorTime(colorTime - 5);
    }
  };

  const startNumberSequence = () => {
    const nums = Array.from({ length: 9 }, (_, i) => i + 1).sort(() => Math.random() - 0.5);
    setNumSequence(nums);
    setNumClicked([]);
    setCurrentGame("number");
    setMsg("Click numbers 1-9 in order!");
  };

  const handleNumberClick = (num) => {
    if (numClicked.length === 0 && num === 1) {
      setNumClicked([1]);
    } else if (numClicked.length > 0 && num === numClicked[numClicked.length - 1] + 1) {
      const newClicked = [...numClicked, num];
      setNumClicked(newClicked);
      if (newClicked.length === 9) {
        setMsg("🎉 Perfect! You completed the sequence!");
      }
    }
  };

  const startQuickReaction = () => {
    setReactionScore(0);
    setReactionReady(false);
    setCurrentGame("reaction");
    setTimeout(() => {
      setReactionColor('#FF6B6B');
      setReactionReady(true);
      setReactionStartTime(Date.now());
    }, 2000);
    setMsg("Wait for the box to turn red, then click!");
  };

  const handleReactionClick = () => {
    if (reactionReady) {
      const time = Date.now() - reactionStartTime;
      setReactionScore(reactionScore + (100 - time));
      setReactionReady(false);
      setMsg("Good! Reaction time: " + time + "ms. Get ready...");
      setTimeout(() => startQuickReaction(), 1000);
    }
  };

  // ========== TEAM MEMBER FUNCTIONS ==========

  const fetchTeamData = async (token) => {
    try {
      const invRes = await fetch(`${API_BASE_URL}/inventory`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (invRes.ok) setInventory(await invRes.json());

      const fundRes = await fetch(`${API_BASE_URL}/funds`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (fundRes.ok) setFunds(await fundRes.json());

      const allocRes = await fetch(`${API_BASE_URL}/fund-allocations`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (allocRes.ok) setFundAllocations(await allocRes.json());

      const distRes = await fetch(`${API_BASE_URL}/distribution/history`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (distRes.ok) setDistributionHistory(await distRes.json());

      const teamRes = await fetch(`${API_BASE_URL}/team-members`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (teamRes.ok) setTeamMembers(await teamRes.json());

      const casesRes = await fetch(`${API_BASE_URL}/cases`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (casesRes.ok) setCases(await casesRes.json());
    } catch (error) {
      console.error("Error fetching team data:", error);
    }
  };

  const addInventoryItem = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!newItemName || !newItemType || !newItemQty) {
      setMsg("All fields required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/inventory/add`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          item_name: newItemName,
          item_type: newItemType,
          quantity: parseInt(newItemQty),
          unit: newItemUnit,
          description: newItemDesc
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Item added successfully!");
        setNewItemName("");
        setNewItemType("");
        setNewItemQty("");
        setNewItemDesc("");
        await fetchTeamData(auth.token);
      } else {
        setMsg("Error: " + (data.error || "Failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const distributeItem = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!distribInventoryId || !distribQty || !distribTo) {
      setMsg("All fields required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/inventory/${distribInventoryId}/distribute`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          quantity: parseInt(distribQty),
          distributed_to: distribTo,
          notes: distribNotes
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Item distributed successfully!");
        setDistribInventoryId("");
        setDistribQty("");
        setDistribTo("");
        setDistribNotes("");
        await fetchTeamData(auth.token);
      } else {
        setMsg("Error: " + (data.error || "Failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const addFunds = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!addFundAmount) {
      setMsg("Amount required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/funds/add`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount: parseFloat(addFundAmount) })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Funds added successfully!");
        setAddFundAmount("");
        await fetchTeamData(auth.token);
      } else {
        setMsg("Error: " + (data.error || "Failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const allocateFunds = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!allocFundParentId || !allocFundAmount) {
      setMsg("Parent ID and amount required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/funds/allocate`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          parent_id: parseInt(allocFundParentId),
          amount: parseFloat(allocFundAmount),
          notes: allocFundNotes
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Funds allocated successfully!");
        setAllocFundParentId("");
        setAllocFundAmount("");
        setAllocFundNotes("");
        await fetchTeamData(auth.token);
      } else {
        setMsg("Error: " + (data.error || "Failed"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  // ========== CASE REPORTING FUNCTIONS (NEW) ==========

  const reportCase = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setMsg("");

    if (!caseLatitude || !caseLongitude || !casePriority || !caseCategory) {
      setMsg("Location, priority, and category required");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/case/report`, {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${auth.token}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          latitude: parseFloat(caseLatitude),
          longitude: parseFloat(caseLongitude),
          location_name: caseLocation,
          priority_level: casePriority,
          description: caseDescription,
          category: caseCategory,
          child_name: caseChildName,
          child_age: caseChildAge ? parseInt(caseChildAge) : null,
          photo_url: casePhoto
        })
      });
      const data = await response.json();

      if (response.ok) {
        setMsg("✅ Case reported successfully!");
        setShowCaseForm(false);
        setCasePhoto("");
        setCaseLatitude("");
        setCaseLongitude("");
        setCaseLocation("");
        setCaseDescription("");
        setCaseChildName("");
        setCaseChildAge("");
        await fetchTeamData(auth.token);
      } else {
        setMsg("Error: " + (data.error || "Failed to report case"));
      }
    } catch (error) {
      setMsg("Error: " + error.message);
    }
    setIsLoading(false);
  };

  const getCurrentLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setCaseLatitude(position.coords.latitude.toFixed(6));
          setCaseLongitude(position.coords.longitude.toFixed(6));
          setMsg("✅ Location captured!");
        },
        (error) => {
          setMsg("❌ Could not get location: " + error.message);
        }
      );
    } else {
      setMsg("❌ Geolocation not supported");
    }
  };

  const logout = () => {
    setAuth({ token: null, user: null, parentName: null, role: null, teamMemberId: null });
    setChildren([]);
    setInventory([]);
    setCases([]);
    setEmail("");
    setPassword("");
    setTeamEmail("");
    setTeamPassword("");
    setParentName("");
    setConfirmPassword("");
    setMsg("");
    setShowHelpSection(false);
    setShowChatbot(false);
    setChatMessages([{ id: 1, type: "bot", text: "Hi! 👋 I'm UpChild Assistant. How can I help you today?" }]);
    setView("welcome");
    setUserType("parent");
  };

  const raiseRequest = async (e) => {
    e.preventDefault();
    if (!requestType || !requestAmount || !requestReason) {
      setMsg("All fields required");
      return;
    }
    const newRequest = {
      id: Date.now(),
      type: requestType,
      amount: requestAmount,
      reason: requestReason,
      date: new Date().toLocaleDateString(),
      status: "Pending"
    };
    setRequests([...requests, newRequest]);
    setMsg("✅ Request submitted successfully!");
    setRequestType("");
    setRequestAmount("");
    setRequestReason("");
    setTimeout(() => setMsg(""), 3000);
  };

  const getPriorityColor = (priority) => {
    switch(priority) {
      case "Critical": return "#FF6B6B";
      case "High": return "#ff9800";
      case "Medium": return "#2196f3";
      case "Low": return "#999";
      default: return "#999";
    }
  };

  const getPriorityBg = (priority) => {
    switch(priority) {
      case "Critical": return "#ffe0e0";
      case "High": return "#fff3cd";
      case "Medium": return "#e7f3ff";
      case "Low": return "#f0f0f0";
      default: return "#f0f0f0";
    }
  };

  // ========== RENDER ==========

  return (
    <div className="app-container">
      {auth.token && userType === "parent" && (
        <>
          <div className={`chatbot-widget ${showChatbot ? 'open' : ''}`}>
            <div className="chatbot-header">
              <h3>💬 UpChild Assistant</h3>
              <button onClick={() => setShowChatbot(false)} className="close-btn">✕</button>
            </div>
            <div className="chatbot-messages">
              {chatMessages.map(msg => (
                <div key={msg.id} className={`chat-message ${msg.type}`}>
                  <p>{msg.text}</p>
                </div>
              ))}
            </div>
            <div className="chatbot-input">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleChatSend()}
                placeholder="Ask..."
                className="chat-input-field"
              />
              <button onClick={handleChatSend} className="send-btn">Send</button>
            </div>
          </div>

          <button
            onClick={() => setShowChatbot(!showChatbot)}
            className="chatbot-toggle-btn"
            title="UpChild Assistant"
          >
            💬
          </button>
        </>
      )}

      {view === "welcome" && (
        <div className="card welcome-card">
          <div className="welcome-header">
            <h1>🎓 Welcome to UpChild</h1>
            <h3>Improving the quality of living</h3>
          </div>
          <div className="button-group">
            <button className="btn btn-primary" onClick={() => { setUserType("parent"); setView("login"); }} disabled={isLoading}>
              👨‍👩‍👧 Parent Login
            </button>
            <button className="btn btn-secondary" onClick={() => { setUserType("parent"); setView("register"); }} disabled={isLoading}>
              📝 Parent Register
            </button>
            <button className="btn btn-primary" onClick={() => { setUserType("team"); setView("team-login"); }} disabled={isLoading} style={{ marginTop: "20px", background: "linear-gradient(135deg, #FF6B6B 0%, #FFA07A 100%)" }}>
              👥 Team Login
            </button>
            <button className="btn btn-secondary" onClick={() => { setUserType("team"); setView("team-register"); }} disabled={isLoading}>
              ✍️ Team Register
            </button>
          </div>
          <footer>(c) 2025 UpChild. All rights reserved.</footer>
        </div>
      )}

      {view === "register" && (
        <div className="card auth-card">
          <h2>Create Account</h2>
          <form onSubmit={register} className="form">
            <input
              type="text"
              placeholder="Parent Name"
              value={parentName}
              onChange={(e) => setParentName(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <button type="submit" disabled={isLoading} className="btn btn-primary">
              {isLoading ? "Creating Account..." : "Register"}
            </button>
          </form>
          <p className="auth-link">Already have an account? <span onClick={() => setView("login")} style={{ cursor: 'pointer', color: '#667eea', fontWeight: 'bold' }}>Login</span></p>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

      {view === "login" && (
        <div className="card auth-card">
          <h2>Login to UpChild</h2>
          <form onSubmit={login} className="form">
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <button type="submit" disabled={isLoading} className="btn btn-primary">
              {isLoading ? "Logging In..." : "Login"}
            </button>
          </form>
          <p className="auth-link">Don't have an account? <span onClick={() => setView("register")} style={{ cursor: 'pointer', color: '#667eea', fontWeight: 'bold' }}>Register</span></p>
          <p className="auth-link" style={{ marginTop: "20px" }}>👥 <span onClick={() => { setUserType("team"); setView("team-login"); }} style={{ cursor: 'pointer', color: '#FF6B6B', fontWeight: 'bold' }}>Team Member Login?</span></p>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

      {view === "team-register" && (
        <div className="card auth-card">
          <h2>Team Member Registration</h2>
          <form onSubmit={teamRegister} className="form">
            <input
              type="text"
              placeholder="Full Name"
              value={teamFullName}
              onChange={(e) => setTeamFullName(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="text"
              placeholder="Username"
              value={teamUsername}
              onChange={(e) => setTeamUsername(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="email"
              placeholder="Email"
              value={teamEmail}
              onChange={(e) => setTeamEmail(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <select
              value={teamRole}
              onChange={(e) => setTeamRole(e.target.value)}
              disabled={isLoading}
              className="input"
            >
              <option value="volunteer">Volunteer</option>
              <option value="manager">Manager</option>
              <option value="admin">Admin</option>
            </select>
            <input
              type="password"
              placeholder="Password"
              value={teamPassword}
              onChange={(e) => setTeamPassword(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <button type="submit" disabled={isLoading} className="btn btn-primary">
              {isLoading ? "Registering..." : "Register"}
            </button>
          </form>
          <p className="auth-link">Already registered? <span onClick={() => setView("team-login")} style={{ cursor: 'pointer', color: '#667eea', fontWeight: 'bold' }}>Login</span></p>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

      {view === "team-login" && (
        <div className="card auth-card">
          <h2>👥 Team Member Login</h2>
          <form onSubmit={teamLogin} className="form">
            <input
              type="email"
              placeholder="Email"
              value={teamEmail}
              onChange={(e) => setTeamEmail(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="password"
              placeholder="Password"
              value={teamPassword}
              onChange={(e) => setTeamPassword(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <button type="submit" disabled={isLoading} className="btn btn-primary">
              {isLoading ? "Logging In..." : "Login"}
            </button>
          </form>
          <p className="auth-link">Don't have an account? <span onClick={() => setView("team-register")} style={{ cursor: 'pointer', color: '#667eea', fontWeight: 'bold' }}>Register</span></p>
          <p className="auth-link" style={{ marginTop: "20px" }}>👨‍👩‍👧 <span onClick={() => { setUserType("parent"); setView("login"); }} style={{ cursor: 'pointer', color: '#4caf50', fontWeight: 'bold' }}>Parent Login?</span></p>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

      {view === "team-dashboard" && (auth.role === "admin" || auth.role === "manager" || auth.role === "volunteer") && (
        <div className="card dashboard-card">
          <div className="dashboard-header">
            <div>
              <h2>👥 Team Member Dashboard</h2>
              <p className="parent-greeting">Welcome, <span className="parent-name">{auth.parentName}</span>! ({auth.role})</p>
            </div>
          </div>

          <div className="tabs">
            <button className={`tab-btn ${teamActiveTab === "cases" ? "active" : ""}`} onClick={() => setTeamActiveTab("cases")}>
              📱 Cases
            </button>
            <button className={`tab-btn ${teamActiveTab === "inventory" ? "active" : ""}`} onClick={() => setTeamActiveTab("inventory")}>
              📦 Inventory
            </button>
            <button className={`tab-btn ${teamActiveTab === "distribution" ? "active" : ""}`} onClick={() => setTeamActiveTab("distribution")}>
              📤 Distribution
            </button>
            <button className={`tab-btn ${teamActiveTab === "funds" ? "active" : ""}`} onClick={() => setTeamActiveTab("funds")}>
              💰 Funds
            </button>
            <button className={`tab-btn ${teamActiveTab === "team" ? "active" : ""}`} onClick={() => setTeamActiveTab("team")}>
              👥 Team
            </button>
          </div>

          {teamActiveTab === "cases" && (
            <>
              <h3>📱 Case Reports (Social Feed)</h3>
              <button 
                className="btn btn-primary" 
                onClick={() => setShowCaseForm(!showCaseForm)}
                style={{ marginBottom: "20px", width: "100%" }}
              >
                {showCaseForm ? "❌ Cancel" : "➕ Report New Case"}
              </button>

              {showCaseForm && (
                <div style={{ background: "#f9f9f9", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
                  <h4>📸 Report a Case</h4>
                  <form onSubmit={reportCase} className="form">
                    <input
                      type="text"
                      placeholder="Photo URL (optional)"
                      value={casePhoto}
                      onChange={(e) => setCasePhoto(e.target.value)}
                      className="input"
                    />
                    <div style={{ display: "flex", gap: "10px" }}>
                      <input
                        type="number"
                        placeholder="Latitude"
                        value={caseLatitude}
                        onChange={(e) => setCaseLatitude(e.target.value)}
                        step="0.000001"
                        className="input"
                        style={{ flex: 1 }}
                      />
                      <input
                        type="number"
                        placeholder="Longitude"
                        value={caseLongitude}
                        onChange={(e) => setCaseLongitude(e.target.value)}
                        step="0.000001"
                        className="input"
                        style={{ flex: 1 }}
                      />
                    </div>
                    <button 
                      type="button" 
                      onClick={getCurrentLocation}
                      className="btn btn-secondary"
                      style={{ width: "100%", marginTop: "5px" }}
                    >
                      📍 Use My Current Location
                    </button>
                    <input
                      type="text"
                      placeholder="Location Name"
                      value={caseLocation}
                      onChange={(e) => setCaseLocation(e.target.value)}
                      className="input"
                    />
                    <select
                      value={casePriority}
                      onChange={(e) => setCasePriority(e.target.value)}
                      className="input"
                    >
                      <option value="Low">Low Priority</option>
                      <option value="Medium">Medium Priority</option>
                      <option value="High">High Priority</option>
                      <option value="Critical">🚨 Critical Priority</option>
                    </select>
                    <select
                      value={caseCategory}
                      onChange={(e) => setCaseCategory(e.target.value)}
                      className="input"
                    >
                      <option value="Child">Child</option>
                      <option value="Family">Family</option>
                      <option value="Medical">Medical</option>
                      <option value="Education">Education</option>
                      <option value="Food">Food</option>
                      <option value="Shelter">Shelter</option>
                      <option value="Other">Other</option>
                    </select>
                    <input
                      type="text"
                      placeholder="Child Name (if applicable)"
                      value={caseChildName}
                      onChange={(e) => setCaseChildName(e.target.value)}
                      className="input"
                    />
                    <input
                      type="number"
                      placeholder="Child Age"
                      value={caseChildAge}
                      onChange={(e) => setCaseChildAge(e.target.value)}
                      className="input"
                    />
                    <textarea
                      placeholder="Description of the case"
                      value={caseDescription}
                      onChange={(e) => setCaseDescription(e.target.value)}
                      className="input"
                      rows="4"
                      required
                    />
                    <button type="submit" className="btn btn-primary" disabled={isLoading}>
                      {isLoading ? "Reporting..." : "📸 Report Case"}
                    </button>
                  </form>
                </div>
              )}

              <h4>📲 Recent Cases Feed</h4>
              <div style={{ maxHeight: "500px", overflowY: "auto" }}>
                {cases.length === 0 ? (
                  <p style={{ textAlign: "center", color: "#999", padding: "20px" }}>No cases reported yet</p>
                ) : (
                  cases.map((caseItem) => (
                    <div 
                      key={caseItem.case_id} 
                      style={{
                        background: getPriorityBg(caseItem.priority_level),
                        borderLeft: `4px solid ${getPriorityColor(caseItem.priority_level)}`,
                        padding: "15px",
                        marginBottom: "12px",
                        borderRadius: "8px",
                        cursor: "pointer",
                        transition: "all 0.3s"
                      }}
                      onClick={() => setSelectedCase(caseItem)}
                    >
                      <div style={{ display: "flex", gap: "12px" }}>
                        {caseItem.photo_url && (
                          <img 
                            src={caseItem.photo_url} 
                            alt="case" 
                            style={{ width: "80px", height: "80px", borderRadius: "8px", objectFit: "cover" }}
                            onError={(e) => { e.target.style.display = 'none'; }}
                          />
                        )}
                        <div style={{ flex: 1 }}>
                          <h5 style={{ margin: "0 0 5px", color: "#333" }}>
                            {caseItem.child_name} • {caseItem.category} 
                            <span style={{
                              background: getPriorityColor(caseItem.priority_level),
                              color: "white",
                              padding: "2px 8px",
                              borderRadius: "12px",
                              fontSize: "11px",
                              marginLeft: "10px"
                            }}>
                              {caseItem.priority_level}
                            </span>
                          </h5>
                          <p style={{ margin: "5px 0", fontSize: "12px", color: "#666" }}>
                            📍 {caseItem.location_name}
                          </p>
                          <p style={{ margin: "5px 0", fontSize: "12px", color: "#999" }}>
                            By {caseItem.reporter_name} • {new Date(caseItem.created_at).toLocaleString()}
                          </p>
                          <p style={{ margin: "5px 0", fontSize: "13px", color: "#333" }}>
                            {caseItem.description.substring(0, 100)}{caseItem.description.length > 100 ? "..." : ""}
                          </p>
                          <span style={{
                            background: caseItem.status === "New" ? "#2196f3" : 
                                       caseItem.status === "In Progress" ? "#ff9800" : 
                                       caseItem.status === "Resolved" ? "#4caf50" : "#999",
                            color: "white",
                            padding: "3px 8px",
                            borderRadius: "12px",
                            fontSize: "10px",
                            marginTop: "8px",
                            display: "inline-block"
                          }}>
                            {caseItem.status}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </>
          )}

          {teamActiveTab === "inventory" && (
            <>
              <h3>📦 Inventory Board</h3>
              <div style={{ background: "#f9f9f9", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
                <h4>Add New Item</h4>
                <form onSubmit={addInventoryItem} className="form">
                  <input
                    type="text"
                    placeholder="Item Name"
                    value={newItemName}
                    onChange={(e) => setNewItemName(e.target.value)}
                    className="input"
                  />
                  <select value={newItemType} onChange={(e) => setNewItemType(e.target.value)} className="input">
                    <option value="">Select Type</option>
                    <option value="Medicine">Medicine</option>
                    <option value="Blanket">Blanket</option>
                    <option value="Book">Book</option>
                    <option value="Money">Money</option>
                    <option value="Food">Food</option>
                    <option value="Other">Other</option>
                  </select>
                  <input
                    type="number"
                    placeholder="Quantity"
                    value={newItemQty}
                    onChange={(e) => setNewItemQty(e.target.value)}
                    className="input"
                  />
                  <select value={newItemUnit} onChange={(e) => setNewItemUnit(e.target.value)} className="input">
                    <option value="pcs">Pieces</option>
                    <option value="box">Box</option>
                    <option value="kg">Kg</option>
                    <option value="liter">Liter</option>
                  </select>
                  <textarea
                    placeholder="Description (optional)"
                    value={newItemDesc}
                    onChange={(e) => setNewItemDesc(e.target.value)}
                    className="input"
                    rows="2"
                  />
                  <button type="submit" disabled={isLoading} className="btn btn-primary">
                    ➕ Add Item
                  </button>
                </form>
              </div>

              <h4>Current Inventory</h4>
              <div className="inventory-table" style={{ overflowX: "auto", marginBottom: "20px" }}>
                <table style={{ width: "100%", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ background: "#667eea", color: "white" }}>
                      <th style={{ padding: "10px", textAlign: "left" }}>Item Name</th>
                      <th style={{ padding: "10px", textAlign: "left" }}>Type</th>
                      <th style={{ padding: "10px", textAlign: "center" }}>Qty</th>
                      <th style={{ padding: "10px", textAlign: "left" }}>Unit</th>
                    </tr>
                  </thead>
                  <tbody>
                    {inventory.map((item) => (
                      <tr key={item.inventory_id} style={{ borderBottom: "1px solid #ddd" }}>
                        <td style={{ padding: "10px" }}>{item.item_name}</td>
                        <td style={{ padding: "10px" }}>{item.item_type}</td>
                        <td style={{ padding: "10px", textAlign: "center", fontWeight: "bold", color: item.quantity < 5 ? "#FF6B6B" : "#4caf50" }}>{item.quantity}</td>
                        <td style={{ padding: "10px" }}>{item.unit}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </>
          )}

          {teamActiveTab === "distribution" && (
            <>
              <h3>📤 Distribution</h3>
              <div style={{ background: "#f9f9f9", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
                <h4>Distribute Item</h4>
                <form onSubmit={distributeItem} className="form">
                  <select
                    value={distribInventoryId}
                    onChange={(e) => setDistribInventoryId(e.target.value)}
                    className="input"
                  >
                    <option value="">Select Item</option>
                    {inventory.map((item) => (
                      <option key={item.inventory_id} value={item.inventory_id}>
                        {item.item_name} (Qty: {item.quantity})
                      </option>
                    ))}
                  </select>
                  <input
                    type="number"
                    placeholder="Quantity to Distribute"
                    value={distribQty}
                    onChange={(e) => setDistribQty(e.target.value)}
                    className="input"
                  />
                  <input
                    type="text"
                    placeholder="Distributed To (Person/Organization)"
                    value={distribTo}
                    onChange={(e) => setDistribTo(e.target.value)}
                    className="input"
                  />
                  <textarea
                    placeholder="Notes (optional)"
                    value={distribNotes}
                    onChange={(e) => setDistribNotes(e.target.value)}
                    className="input"
                    rows="2"
                  />
                  <button type="submit" disabled={isLoading} className="btn btn-primary">
                    ✅ Distribute
                  </button>
                </form>
              </div>

              <h4>Distribution History</h4>
              <div style={{ maxHeight: "300px", overflowY: "auto" }}>
                {distributionHistory.map((log) => (
                  <div key={log.log_id} style={{ background: "#f5f5f5", padding: "12px", marginBottom: "10px", borderRadius: "8px", borderLeft: "4px solid #667eea" }}>
                    <p><strong>Item ID:</strong> {log.inventory_id} | <strong>Qty:</strong> {log.quantity}</p>
                    <p><strong>Distributed To:</strong> {log.distributed_to}</p>
                    <p><strong>Date:</strong> {log.date}</p>
                    {log.notes && <p><strong>Notes:</strong> {log.notes}</p>}
                  </div>
                ))}
              </div>
            </>
          )}

          {teamActiveTab === "funds" && (
            <>
              <h3>💰 Fund Management</h3>
              <div style={{ background: "linear-gradient(135deg, #4caf50 0%, #45a049 100%)", color: "white", padding: "20px", borderRadius: "10px", marginBottom: "20px", textAlign: "center" }}>
                <p style={{ margin: 0, fontSize: "12px" }}>Total Available</p>
                <h2 style={{ margin: "10px 0 0" }}>₹{funds.total_available}</h2>
                <p style={{ margin: "10px 0 0", fontSize: "12px" }}>Allocated: ₹{funds.total_allocated} | Distributed: ₹{funds.total_distributed}</p>
              </div>

              <div style={{ background: "#f9f9f9", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
                <h4>Add Funds</h4>
                <form onSubmit={addFunds} className="form">
                  <input
                    type="number"
                    placeholder="Amount (₹)"
                    value={addFundAmount}
                    onChange={(e) => setAddFundAmount(e.target.value)}
                    className="input"
                    step="0.01"
                  />
                  <button type="submit" disabled={isLoading} className="btn btn-primary">
                    ➕ Add Funds
                  </button>
                </form>
              </div>

              <div style={{ background: "#f9f9f9", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
                <h4>Allocate Funds to Parent</h4>
                <form onSubmit={allocateFunds} className="form">
                  <input
                    type="number"
                    placeholder="Parent ID"
                    value={allocFundParentId}
                    onChange={(e) => setAllocFundParentId(e.target.value)}
                    className="input"
                  />
                  <input
                    type="number"
                    placeholder="Amount (₹)"
                    value={allocFundAmount}
                    onChange={(e) => setAllocFundAmount(e.target.value)}
                    className="input"
                    step="0.01"
                  />
                  <textarea
                    placeholder="Notes (optional)"
                    value={allocFundNotes}
                    onChange={(e) => setAllocFundNotes(e.target.value)}
                    className="input"
                    rows="2"
                  />
                  <button type="submit" disabled={isLoading} className="btn btn-primary">
                    💸 Allocate
                  </button>
                </form>
              </div>

              <h4>Fund Allocations</h4>
              <div style={{ maxHeight: "300px", overflowY: "auto" }}>
                {fundAllocations.map((alloc) => (
                  <div key={alloc.allocation_id} style={{ background: "#fff3cd", padding: "12px", marginBottom: "10px", borderRadius: "8px", borderLeft: "4px solid #ff9800" }}>
                    <p><strong>Parent ID:</strong> {alloc.parent_id} | <strong>Amount:</strong> ₹{alloc.amount}</p>
                    <p><strong>Status:</strong> {alloc.status} | <strong>Date:</strong> {alloc.date}</p>
                    {alloc.notes && <p><strong>Notes:</strong> {alloc.notes}</p>}
                  </div>
                ))}
              </div>
            </>
          )}

          {teamActiveTab === "team" && (
            <>
              <h3>👥 Team Members</h3>
              <div style={{ maxHeight: "400px", overflowY: "auto" }}>
                {teamMembers.map((member) => (
                  <div key={member.team_member_id} style={{ background: "linear-gradient(135deg, #e0e7ff 0%, #f3e5f5 100%)", padding: "15px", marginBottom: "10px", borderRadius: "8px", borderLeft: "4px solid #667eea" }}>
                    <p><strong>{member.full_name}</strong></p>
                    <p>Email: {member.email}</p>
                    <p>Role: <span style={{ background: "#667eea", color: "white", padding: "3px 8px", borderRadius: "12px", fontSize: "12px" }}>{member.role}</span></p>
                    <p>Status: {member.status === "active" ? "✅ Active" : "❌ Inactive"}</p>
                  </div>
                ))}
              </div>
            </>
          )}

          <button className="btn btn-secondary" onClick={logout} style={{ marginTop: "20px", width: "100%" }}>
            🚪 Logout
          </button>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

{view === "dashboard" && userType === "parent" && (
        <div className="card dashboard-card">
          <div className="dashboard-header">
            <div>
              <h2>Dashboard</h2>
              <p className="parent-greeting">👋 Welcome, <span className="parent-name">{auth.parentName}</span>!</p>
            </div>
            <button
              className="help-access-btn"
              onClick={() => setShowHelpSection(!showHelpSection)}
              title="Health & Support Resources"
            >
              🏥 Help & Support
            </button>
          </div>

          {showHelpSection ? (
            <>
              <h3>🏥 Health & Help Resources</h3>
              <p className="section-subtitle">Connect with professionals and support organizations</p>

              <div className="resources-grid">
                {healthResources.map((resource, idx) => (
                  <div key={idx} className="resource-card">
                    <div className="resource-icon">{resource.icon}</div>
                    <h4>{resource.type}</h4>
                    <p className="resource-desc">{resource.description}</p>
                    <p className="resource-services"><strong>Services:</strong></p>
                    <ul className="services-list">
                      {resource.services.map((service, i) => (
                        <li key={i}>✓ {service}</li>
                      ))}
                    </ul>
                    <p className="resource-contact"><strong>📞</strong> {resource.contact}</p>
                    <p className="resource-email"><strong>📧</strong> {resource.email}</p>
                  </div>
                ))}
              </div>

              <div className="funding-section">
                <h3>💰 Raise Funding Request</h3>
                <form onSubmit={raiseRequest} className="form">
                  <select
                    value={requestType}
                    onChange={(e) => setRequestType(e.target.value)}
                    className="input"
                  >
                    <option value="">Select Request Type</option>
                    <option value="Medical">Medical Support</option>
                    <option value="Education">Education Support</option>
                    <option value="Nutrition">Nutrition & Food</option>
                    <option value="Shelter">Shelter & Housing</option>
                    <option value="Other">Other</option>
                  </select>
                  <input
                    type="number"
                    placeholder="Requested Amount (₹)"
                    value={requestAmount}
                    onChange={(e) => setRequestAmount(e.target.value)}
                    className="input"
                  />
                  <textarea
                    placeholder="Reason & Details"
                    value={requestReason}
                    onChange={(e) => setRequestReason(e.target.value)}
                    className="input"
                    rows="3"
                  />
                  <button type="submit" className="btn btn-primary">
                    Submit Request
                  </button>
                </form>

                {requests.length > 0 && (
                  <>
                    <h3 style={{ marginTop: "30px" }}>Your Requests</h3>
                    <div className="requests-list">
                      {requests.map((req) => (
                        <div key={req.id} className="request-card">
                          <div className="request-header">
                            <p><strong>{req.type}</strong></p>
                            <span className="status-badge">{req.status}</span>
                          </div>
                          <p className="request-amount">₹{req.amount}</p>
                          <p className="request-date">Date: {req.date}</p>
                        </div>
                      ))}
                    </div>
                  </>
                )}
              </div>

              <button
                className="btn btn-secondary"
                onClick={() => setShowHelpSection(false)}
                style={{ marginTop: "20px", width: "100%" }}
              >
                ← Back to Children
              </button>
            </>
          ) : (
            <>
              <h3>👶 Your Children</h3>
              {isLoading ? (
                <p className="loading-text">Loading children...</p>
              ) : children.length === 0 ? (
                <p className="empty-text">No children added yet. Click "Add Child" to get started!</p>
              ) : (
                <ul className="child-list">
                  {children.map((child) => (
                    <li
                      key={child.child_id}
                      className="child-item"
                      onClick={() => fetchChildDetails(child.child_id)}
                    >
                      <div className="child-avatar">👧</div>
                      <div className="child-info-box">
                        <strong>{child.name}</strong><br />
                        <small>DOB: {child.birth_date}</small>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </>
          )}

          <div className="button-group">
            <button className="btn btn-primary" onClick={() => setView("add-child")}>
              ➕ Add Child
            </button>
            <button className="btn btn-primary" onClick={fetchChildren} disabled={isLoading}>
              🔄 Refresh
            </button>
            <button className="btn btn-secondary" onClick={logout}>
              🚪 Logout
            </button>
          </div>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

      {view === "add-child" && (
        <div className="card">
          <h2>Add New Child</h2>
          <form onSubmit={addChild} className="form">
            <input
              type="text"
              placeholder="Child Name"
              value={childName}
              onChange={(e) => setChildName(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <input
              type="date"
              value={childBirthDate}
              onChange={(e) => setChildBirthDate(e.target.value)}
              disabled={isLoading}
              className="input"
            />
            <select
              value={childGender}
              onChange={(e) => setChildGender(e.target.value)}
              disabled={isLoading}
              className="input"
            >
              <option value="">Select Gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
            <button type="submit" disabled={isLoading} className="btn btn-primary">
              {isLoading ? "Adding..." : "Add Child"}
            </button>
          </form>
          <button className="btn btn-secondary" onClick={() => setView("dashboard")} disabled={isLoading}>
            Back
          </button>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}

      {view === "child-details" && childDetails && (
        <div className="card card-large">
          <h2>{childDetails.name}</h2>
          <div className="child-info">
            <p>Birth Date: {childDetails.birth_date}</p>
            <p>Gender: {childDetails.gender}</p>
          </div>

          <div className="tabs">
            <button
              className={`tab-btn ${activeTab === "health" ? "active" : ""}`}
              onClick={() => setActiveTab("health")}
            >
              Health
            </button>
            <button
              className={`tab-btn ${activeTab === "behavior" ? "active" : ""}`}
              onClick={() => setActiveTab("behavior")}
            >
              Behavior
            </button>
            <button
              className={`tab-btn ${activeTab === "manner" ? "active" : ""}`}
              onClick={() => setActiveTab("manner")}
            >
              Manners
            </button>
            <button
              className={`tab-btn ${activeTab === "games" ? "active" : ""}`}
              onClick={() => setActiveTab("games")}
            >
              Games
            </button>
            <button
              className={`tab-btn ${activeTab === "goals" ? "active" : ""}`}
              onClick={() => setActiveTab("goals")}
            >
              Goals
            </button>
          </div>

          {activeTab === "health" && (
            <>
              <h3>Health Records</h3>
              {childDetails.health_records && childDetails.health_records.length > 0 ? (
                <div className="health-records">
                  {childDetails.health_records.map((record) => (
                    <div key={record.record_id} className="record-card">
                      <p><strong>Date:</strong> {record.date}</p>
                      <p><strong>Height:</strong> {record.height} cm | <strong>Weight:</strong> {record.weight} kg</p>
                      <p><strong>BMI:</strong> {calculateBMI(record.weight, record.height)} ({getBMICategory(calculateBMI(record.weight, record.height))})</p>
                    </div>
                  ))}
                </div>
              ) : (
                <p>No health records.</p>
              )}

              <h3>Add Health Record</h3>
              <form onSubmit={addHealthRecord} className="form">
                <input
                  type="date"
                  value={recordDate}
                  onChange={(e) => setRecordDate(e.target.value)}
                  disabled={isLoading}
                  className="input"
                />
                <input
                  type="number"
                  placeholder="Height (cm)"
                  value={height}
                  onChange={(e) => setHeight(e.target.value)}
                  disabled={isLoading}
                  className="input"
                  step="0.1"
                />
                <input
                  type="number"
                  placeholder="Weight (kg)"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  disabled={isLoading}
                  className="input"
                  step="0.1"
                />
                <textarea
                  placeholder="Notes"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  disabled={isLoading}
                  className="input"
                  rows="2"
                />
                <button type="submit" disabled={isLoading} className="btn btn-primary">
                  Add Record
                </button>
              </form>
            </>
          )}

          {activeTab === "behavior" && (
            <>
              <h3>Behavior Tracking</h3>
              <p>Track child's emotional and behavioral patterns over time.</p>
              <div className="behavior-list">
                <div className="behavior-card">
                  <p><strong>Happy</strong> - Joyful and satisfied</p>
                </div>
                <div className="behavior-card">
                  <p><strong>Calm</strong> - Peaceful and relaxed</p>
                </div>
                <div className="behavior-card">
                  <p><strong>Excited</strong> - Enthusiastic and energetic</p>
                </div>
              </div>
            </>
          )}

          {activeTab === "manner" && (
            <>
              <h3>Basic Manner Training</h3>
              <div className="manner-skills">
                <div className="skill-card">
                  <p><strong>🙏 Respect & Courtesy</strong></p>
                  <p>Teaching respect to elders and polite behavior</p>
                </div>
                <div className="skill-card">
                  <p><strong>🤝 Social Skills</strong></p>
                  <p>Communication and interaction with peers</p>
                </div>
                <div className="skill-card">
                  <p><strong>🍴 Table Manners</strong></p>
                  <p>Dining etiquette and behavior</p>
                </div>
                <div className="skill-card">
                  <p><strong>📚 Discipline</strong></p>
                  <p>Following rules and instructions</p>
                </div>
              </div>
            </>
          )}

          {activeTab === "games" && (
            <>
              {currentGame === null ? (
                <>
                  <h3>🎮 Brain Development Games</h3>
                  <p>Have fun while improving cognitive skills!</p>

                  <div className="games-grid">
                    <div className="game-card" onClick={startColorMatch}>
                      <div className="game-icon">🎨</div>
                      <h4>Color Match</h4>
                      <p>Match Colors Fast</p>
                    </div>
                    <div className="game-card" onClick={startNumberSequence}>
                      <div className="game-icon">🔢</div>
                      <h4>Sequence</h4>
                      <p>Order 1-9</p>
                    </div>
                    <div className="game-card" onClick={startQuickReaction}>
                      <div className="game-icon">⚡</div>
                      <h4>Reaction</h4>
                      <p>Speed Test</p>
                    </div>
                  </div>
                </>
              ) : currentGame === "color" ? (
                <>
                  <h3>Color Match</h3>
                  <div style={{ marginBottom: '20px', fontSize: '24px', fontWeight: 'bold', color: '#667eea' }}>
                    Score: {colorScore} | Time: {colorTime}s
                  </div>

                  <div className="target-color" style={{ backgroundColor: colorOptions[colorTargetIdx] }}>
                    Match This Color!
                  </div>

                  <div className="color-grid">
                    {colorOptions.map((color, idx) => (
                      <div
                        key={idx}
                        className="color-tile"
                        style={{ backgroundColor: color }}
                        onClick={() => handleColorClick(idx)}
                      />
                    ))}
                  </div>
                  <button className="btn btn-secondary" onClick={() => setCurrentGame(null)}>
                    Quit
                  </button>
                </>
              ) : currentGame === "number" ? (
                <>
                  <h3>Number Sequence</h3>
                  <div style={{ marginBottom: '20px', fontSize: '18px', color: '#667eea' }}>
                    Click: {numClicked.length === 0 ? "1" : numClicked[numClicked.length - 1] + 1}
                  </div>

                  <div className="number-grid">
                    {numSequence.map((num, idx) => (
                      <button
                        key={idx}
                        className={`number-tile ${numClicked.includes(num) ? 'clicked' : ''}`}
                        onClick={() => handleNumberClick(num)}
                        disabled={numClicked.includes(num)}
                      >
                        {num}
                      </button>
                    ))}
                  </div>
                  <button className="btn btn-secondary" onClick={() => setCurrentGame(null)}>
                    Quit
                  </button>
                </>
              ) : currentGame === "reaction" ? (
                <>
                  <h3>Quick Reaction</h3>
                  <div style={{ marginBottom: '20px', fontSize: '20px', color: '#667eea' }}>
                    Score: {Math.max(0, Math.round(reactionScore))}
                  </div>

                  <div
                    className="reaction-box"
                    style={{
                      backgroundColor: reactionColor,
                      cursor: reactionReady ? 'pointer' : 'default'
                    }}
                    onClick={handleReactionClick}
                  >
                    {!reactionReady ? "Wait..." : "Click!"}
                  </div>
                  <button className="btn btn-secondary" onClick={() => setCurrentGame(null)}>
                    Quit
                  </button>
                </>
              ) : null}
              {msg && <p className="message">{msg}</p>}
            </>
          )}

          {activeTab === "goals" && (
            <>
              <h3>🎯 Goals & Milestones</h3>
              
              <button 
                className="btn btn-primary" 
                onClick={() => setShowGoalForm(!showGoalForm)}
                style={{ marginBottom: "20px", width: "100%" }}
              >
                {showGoalForm ? "❌ Cancel" : "➕ Add New Goal"}
              </button>

              {showGoalForm && (
                <div style={{ background: "#f9f9f9", padding: "20px", borderRadius: "10px", marginBottom: "20px" }}>
                  <h4>📝 Create a New Goal</h4>
                  <form onSubmit={addGoal} className="form">
                    <textarea
                      placeholder="Goal Description (e.g., Learn to read fluently, Improve math skills)"
                      value={goalDescription}
                      onChange={(e) => setGoalDescription(e.target.value)}
                      className="input"
                      rows="3"
                      disabled={isLoading}
                    />
                    <input
                      type="date"
                      value={goalTargetDate}
                      onChange={(e) => setGoalTargetDate(e.target.value)}
                      className="input"
                      disabled={isLoading}
                    />
                    <button type="submit" disabled={isLoading} className="btn btn-primary" style={{ width: "100%" }}>
                      {isLoading ? "Adding..." : "✓ Create Goal"}
                    </button>
                  </form>
                </div>
              )}

              {childDetails.goals && childDetails.goals.length > 0 ? (
                <>
                  <div style={{ marginBottom: "15px", padding: "10px", background: "rgba(102, 126, 234, 0.1)", borderRadius: "8px" }}>
                    <p style={{ margin: "0", color: "#333" }}>
                      <strong>Progress:</strong> {childDetails.goals.filter(g => g.is_completed).length} of {childDetails.goals.length} goals completed
                    </p>
                    <div style={{
                      width: "100%",
                      height: "20px",
                      background: "#e0e0e0",
                      borderRadius: "10px",
                      marginTop: "8px",
                      overflow: "hidden"
                    }}>
                      <div style={{
                        height: "100%",
                        width: `${(childDetails.goals.filter(g => g.is_completed).length / childDetails.goals.length) * 100}%`,
                        background: "linear-gradient(90deg, #667eea 0%, #764ba2 100%)",
                        transition: "width 0.3s ease"
                      }} />
                    </div>
                  </div>

                  <div className="goals-list">
                    {childDetails.goals.map((goal) => (
                      <div key={goal.goal_id} className="goal-card" style={{
                        background: goal.is_completed 
                          ? "linear-gradient(135deg, #d4edda 0%, #c8e6c9 100%)"
                          : "linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%)",
                        padding: "15px",
                        borderRadius: "10px",
                        marginBottom: "12px",
                        border: `2px solid ${goal.is_completed ? "#4caf50" : "#ff9800"}`,
                        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.08)",
                        transition: "all 0.3s ease"
                      }}>
                        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "start", gap: "10px" }}>
                          <div style={{ flex: 1 }}>
                            <p style={{
                              margin: "0 0 8px 0",
                              fontSize: "1.05rem",
                              fontWeight: "bold",
                              color: "#333",
                              textDecoration: goal.is_completed ? "line-through" : "none",
                              opacity: goal.is_completed ? 0.7 : 1
                            }}>
                              {goal.description}
                            </p>
                            <p style={{ margin: "5px 0", color: "#666", fontSize: "0.9rem" }}>
                              📅 Target: {new Date(goal.target_date).toLocaleDateString()}
                            </p>
                            <p style={{
                              margin: "5px 0",
                              fontSize: "0.9rem",
                              fontWeight: "600",
                              color: goal.is_completed ? "#4caf50" : "#ff9800"
                            }}>
                              {goal.is_completed ? "✅ Completed" : "⏳ In Progress"}
                            </p>
                          </div>
                          <div style={{ display: "flex", gap: "8px", flexDirection: "column" }}>
                            <button
                              onClick={() => toggleGoalCompletion(goal.goal_id)}
                              className="btn"
                              style={{
                                padding: "8px 12px",
                                fontSize: "0.85rem",
                                background: goal.is_completed ? "#4caf50" : "#2196f3",
                                color: "white",
                                border: "none",
                                borderRadius: "6px",
                                cursor: "pointer",
                                transition: "all 0.2s ease"
                              }}
                              disabled={isLoading}
                            >
                              {goal.is_completed ? "↩️ Undo" : "✓ Mark Done"}
                            </button>
                            <button
                              onClick={() => deleteGoal(goal.goal_id)}
                              className="btn"
                              style={{
                                padding: "8px 12px",
                                fontSize: "0.85rem",
                                background: "#f44336",
                                color: "white",
                                border: "none",
                                borderRadius: "6px",
                                cursor: "pointer",
                                transition: "all 0.2s ease"
                              }}
                              disabled={isLoading}
                            >
                              🗑️ Delete
                            </button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p style={{
                  textAlign: "center",
                  color: "#999",
                  padding: "30px",
                  fontSize: "1rem"
                }}>
                  📌 No goals set yet. Click "Add New Goal" to create one!
                </p>
              )}
            </>
          )}

          <button className="btn btn-secondary" onClick={() => setView("dashboard")}>
            Back to Dashboard
          </button>
          {msg && <p className="message">{msg}</p>}
        </div>
      )}
    </div>
  );
}

