import React,{createContext,useContext,useEffect,useState} from "react";
const WishlistContext=createContext(null);
export function WishlistProvider({children}){
 const [items,setItems]=useState(()=>{try{return JSON.parse(localStorage.getItem("sidra-fabrics_wishlist"))||[]}catch{return[]}});
 useEffect(()=>localStorage.setItem("sidra-fabrics_wishlist",JSON.stringify(items)),[items]);
 const isWishlisted=id=>items.some(i=>String(i.id)===String(id));
 const toggleWishlist=p=>setItems(x=>isWishlisted(p.id)?x.filter(i=>String(i.id)!==String(p.id)):[...x,p]);
 const removeFromWishlist=id=>setItems(x=>x.filter(i=>String(i.id)!==String(id)));
 return <WishlistContext.Provider value={{items,isWishlisted,toggleWishlist,removeFromWishlist,clearWishlist:()=>setItems([])}}>{children}</WishlistContext.Provider>
}
export function useWishlist(){const c=useContext(WishlistContext);if(!c)throw new Error("useWishlist must be inside WishlistProvider");return c}
