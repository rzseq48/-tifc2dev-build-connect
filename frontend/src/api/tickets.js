import api from "./client";
export async function getTickets(){const r=await api.get("/tickets");return r.data;}
export async function getTicket(id){const r=await api.get(`/tickets/${id}`);return r.data;}
export async function createTicket(data){const r=await api.post("/tickets",data);return r.data;}
export async function updateTicket(id,changes){const r=await api.patch(`/tickets/${id}`,changes);return r.data;}
export async function deleteTicket(id){const r=await api.delete(`/tickets/${id}`);return r.data;}
