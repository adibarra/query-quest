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
  id: string
  question: string
  difficulty: number
  options: string[]
  tags: string[]
}

export interface Tag {
  id: string
  name: string
  description: string
}

export interface Stats {
  wins: number
  losses: number
  xp: number
}
