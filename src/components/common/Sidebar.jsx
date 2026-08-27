import React from "react";
import {Link} from "react-router-dom";
export default function Sidebar({open,onClose}){
 return <div className={`mobile-sidebar ${open?"open":""}`}><div className="mobile-sidebar-head"><b>SIDRA FABRICS</b><button onClick={onClose}>×</button></div><Link onClick={onClose} to="/shop">Shop all</Link><Link onClick={onClose} to="/shop?cat=women-clothing">Women clothing</Link><Link onClick={onClose} to="/shop?cat=shoes">Shoes</Link><Link onClick={onClose} to="/shop?cat=women-fragrance">Fragrance</Link><Link onClick={onClose} to="/shop?sale=1">Sale</Link><Link onClick={onClose} to="/track">Track order</Link></div>
}
