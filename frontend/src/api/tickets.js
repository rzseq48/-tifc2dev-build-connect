import api from "./client";
export async function getTickets(){const r=await api.get("/tickets");return r.data;}
export async function getTicket(id){const r=await api.get(`/tickets/${id}`);return r.data;}
export async function createTicket(data){throw new Error("TODO LAB 3: createTicket");}
export async function updateTicket(id,changes){throw new Error("TODO LAB 3: updateTicket");}
export async function deleteTicket(id){throw new Error("TODO LAB 3: deleteTicket");}
