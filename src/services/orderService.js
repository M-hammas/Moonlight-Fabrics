import api from "./api";
export const orderService={
 create:(data)=>api.post("/orders",data),
 myOrders:()=>api.get("/orders/my"),
 get:(id)=>api.get(`/orders/${id}`),
 updateStatus:(id,status)=>api.patch(`/orders/${id}/status`,{status})
};
