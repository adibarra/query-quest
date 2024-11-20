/**
 * @author: adibarra (Alec Ibarra)
 * @description: Typescript types definitions
 */

import type { App } from 'vue'
import type { Router } from 'vue-router'

export type UserModule = (ctx: { app: App, router: Router }) => void

export interface Session {
  user_uuid: string
  token: string
  created_at: string
}

export interface User {
  uuid: string
  username: string
}

export interface Question {
  id: number
  question: string
  difficulty: number
  options: string[]
  tags: number[]
}

export interface Tag {
  id: number
  name: string
  description: string
}

export interface Stats {
  user_uuid: string
  wins: number
  losses: number
  xp: number
}
