import { useState, useEffect } from "react"


export default function HomePage() {
    const [username,setUsername]= useState('')
    const [password,setPassword] = useState('')

    const  submitHandler = async ()=>{
        const result = await fetch('http://localhost:5000/fetchFromForm',{
            method:'POST',
            headers:{
                "Content-Type":'application/json'
            },
            body: JSON.stringify({
                'username':username,
                'password':password
            })
        })
        const response = await result.json()
        console.log(response.username,response.password)
    }
    return (
<div>
        <div className="flex flex-col gap-5">
            <input onChange={(e)=>{setUsername(e.target.value)}} className="border border-black border-solid w-[40%]" type="text" />
            <input onChange={(e)=>{setPassword(e.target.value)}} type="text" className=" w-[40%] border border-solid border-black" />
            <button onClick={()=>submitHandler()} type="submit">Submit</button>
        </div>
</div>
    )
}