"use client"

import { SkillsTag } from '../../../alumnator/app/profiles/components/SkillsTag'
import SkillsCollapsible from '../../../alumnator/app/profiles/components/SkillsCollapsible'
import DomainForm from './components/DomainForm'
import { TagInt } from '../../../alumnator/app/definitions'

import * as React from "react"

import { useEffect, useState } from 'react'

export default function Profiles(){
    const [tags, setTags] = React.useState<TagInt[]>([]) 

    return(
        <div className="h-full flex">
           <div className="h-full w-3/4 ml-16 flex justify-center items-start">
                <DomainForm tags={tags} setTags={setTags}/>
           </div>
           <div className="h-full w-1/4 mr-16 flex justify-center items-center">
                <SkillsCollapsible tags={tags} />
           </div>
        </div>
    )
}