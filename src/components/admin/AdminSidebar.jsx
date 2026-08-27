import React from "react";import {NavLink} from "react-router-dom";
export default function AdminSidebar(){
 const links=[["/admin","Overview"],["/admin/products","Products"],["/admin/orders","Orders"],["/admin/commerce","Commerce"],["/admin/settings","Settings"]];
 return <aside className="admin-sidebar"><div className="admin-brand">SIDRA FABRICS<span>ADMIN</span></div>{links.map(([to,label])=><NavLink end={to==="/admin"} className={({isActive})=>isActive?"active":""} to={to} key={to}>{label}</NavLink>)}<NavLink to="/">← Storefront</NavLink></aside>
}
