import React,{createContext,useContext,useEffect,useMemo,useState} from "react";
const CartContext=createContext(null);
export function CartProvider({children}){
 const [items,setItems]=useState(()=>{try{return JSON.parse(localStorage.getItem("sidra-fabrics_cart"))||[]}catch{return[]}});
 useEffect(()=>localStorage.setItem("sidra-fabrics_cart",JSON.stringify(items)),[items]);
 const addToCart=(product,quantity=1)=>setItems(x=>{const found=x.find(i=>String(i.id)===String(product.id));return found?x.map(i=>String(i.id)===String(product.id)?{...i,quantity:i.quantity+quantity}:i):[...x,{...product,quantity}]});
 const removeFromCart=id=>setItems(x=>x.filter(i=>String(i.id)!==String(id)));
 const updateQuantity=(id,quantity)=>quantity<=0?removeFromCart(id):setItems(x=>x.map(i=>String(i.id)===String(id)?{...i,quantity}:i));
 const clearCart=()=>setItems([]);
 const subtotal=items.reduce((s,i)=>s+Number(i.salePrice??i.price)*i.quantity,0);
 const itemCount=items.reduce((s,i)=>s+i.quantity,0);
 return <CartContext.Provider value={useMemo(()=>({items,addToCart,removeFromCart,updateQuantity,clearCart,subtotal,itemCount}),[items,subtotal,itemCount])}>{children}</CartContext.Provider>
}
export function useCart(){const c=useContext(CartContext);if(!c)throw new Error("useCart must be inside CartProvider");return c}
