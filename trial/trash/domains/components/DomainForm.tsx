import * as React from "react"

import { Button } from "@/components/ui/button"
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"

import { SkillsTag } from "@/app/profiles/components/SkillsTag"
import { TagsInterface } from '../../../../alumnator/app/definitions'
import axios from 'axios'

export default function DomainForm(props: TagsInterface) {
  const tags = props.tags
  const setTags = props.setTags
  
  async function createDomain(event:any){
    event.preventDefault()
    const name = event.target.domainName.value

    console.log("NAME", name)
    const baseURL = `http://localhost:3002/api/domains`
    const domain = {
      "name": name,
      "lower_name": name.toLowerCase(),
      "skills": tags.map((tag) => tag._id)
    }
    console.log(domain)
    axios.post(baseURL, domain)
        .then((response) => {
            setTags([])
        }).catch((error) => {
          console.log("ERROR WHILE CREATING THE DOMAIN.")
        })
  }

  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Create a new domain</CardTitle>
        <CardDescription>Group multiple skills under a domain.</CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={createDomain}>
          <div className="grid w-full items-center gap-4">
            <div className="flex flex-col space-y-1.5">
              <Label htmlFor="name">Name</Label>
              <Input id="domainName" placeholder="Name of the domain" name="domainName"/>
            </div>
            <div className="flex flex-col space-y-1.5 items-start">
              <Label htmlFor="skills">Skills</Label>
              <SkillsTag tags={tags} setTags={setTags} />
            </div>
          </div>
          <div className="flex justify-end mt-8">
            <Button type="submit">Create</Button>
          </div>
        </form>
      </CardContent>
      
    </Card>
  )
}
