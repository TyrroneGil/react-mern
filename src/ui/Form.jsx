import { useState } from "react";


export default function Form(props){



    return(
        
        <div className="w-[40%] h-[40%] bg-slate-400 flex flex-col p-5 justify-between ">
            <input className="border border-black"  type="text" />
            <input className="border border-black"  />
            <input type="checkbox"/>
            <button className="border bg-black text-white" >Submit</button>
        </div>
        


    );
}