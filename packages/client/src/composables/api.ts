/**
 * @author: adibarra (Alec Ibarra)
 * @description: Composable for providing access to the QueryQuest API
 */
import { type AfterFetchContext, type OnFetchErrorContext, StorageSerializers, type UseFetchReturn } from '@vueuse/core'
import type { Question, Session, Stats, Tag, User } from '~/types'

const session = useSessionStorage<Session | null>('query-quest/session', null, { serializer: StorageSerializers.object })

export enum API_STATUS {
  OK = 200,
  CREATED = 201,
  BAD_REQUEST = 400,
  UNAUTHORIZED = 401,
  FORBIDDEN = 403,
  NOT_FOUND = 404,
  CONFLICT = 409,
  ERROR = 500,
  TIMEOUT = -1,
  OUTDATED = -2,
}

/**
 * Recursively expands a type to see its shape instead of type names.
 * Source: https://stackoverflow.com/a/69288824
 */
type ExpandRecursively<T> = T extends (...args: infer A) => infer R
  ? (...args: ExpandRecursively<A>) => ExpandRecursively<R>
  : T extends object
    ? T extends infer O
      ? { [K in keyof O]: ExpandRecursively<O[K]> }
      : never
    : T

/**
 * Composable function to use the QueryQuest API
 * @param options (optional) options for the API
 * @param options.base (optional) the base URL of the API
 * @returns an object with functions to interact with the API
 */
export function useAPI(options?: { base?: string }) {
  const API_BASE = options?.base ?? import.meta.env.DEV ? 'http://localhost:3332/api/v1' : 'https://quest-api.adibarra.com/api/v1'

  enum API_QUERY {
    POST_SESSION, DELETE_SESSION,
    POST_USER, GET_USER, UPDATE_USER, DELETE_USER,
    POST_QUESTION, GET_QUESTION,
    GET_QUESTIONS,
    GET_TAGS,
    GET_STATS, UPDATE_STATS,
    SUBMIT_ANSWER,
  }

  const latestCompletedTimestamps: Record<API_QUERY, number> = {
    [API_QUERY.POST_SESSION]: 0,
    [API_QUERY.DELETE_SESSION]: 0,
    [API_QUERY.POST_USER]: 0,
    [API_QUERY.GET_USER]: 0,
    [API_QUERY.UPDATE_USER]: 0,
    [API_QUERY.DELETE_USER]: 0,
    [API_QUERY.POST_QUESTION]: 0,
    [API_QUERY.GET_QUESTION]: 0,
    [API_QUERY.GET_QUESTIONS]: 0,
    [API_QUERY.GET_TAGS]: 0,
    [API_QUERY.GET_STATS]: 0,
    [API_QUERY.UPDATE_STATS]: 0,
    [API_QUERY.SUBMIT_ANSWER]: 0,
  }

  function setSession(ctx: AfterFetchContext) {
    session.value = ctx.data.data
    return ctx
  }

  function clearSession(ctx: AfterFetchContext | OnFetchErrorContext) {
    session.value = null
    return ctx
  }

  return {
    /**
     * Get the current session
     */
    getSession: () => session.value,
    /**
     * Create a new session
     * @param data
     * @param data.username the user's username
     * @param data.password the user's password
     * @returns a new session object if successful
     */
    auth: async (data: { username: string, password: string }): Promise<API_RESPONSE[API_QUERY.POST_SESSION]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(removeEmpty(data)),
      }, { afterFetch: setSession, timeout: 3333 }).json<API_RESPONSE[API_QUERY.POST_SESSION]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.POST_SESSION]) {
        latestCompletedTimestamps[API_QUERY.POST_SESSION] = requestTimestamp
        return handleErrors<API_QUERY.POST_SESSION>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Delete a session associated with a token
     */
    deauth: async (): Promise<API_RESPONSE[API_QUERY.DELETE_SESSION]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/sessions`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${session.value?.token}`,
        },
      }, { afterFetch: clearSession, onFetchError: clearSession, timeout: 3333 }).json<API_RESPONSE[API_QUERY.DELETE_SESSION]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.DELETE_SESSION]) {
        latestCompletedTimestamps[API_QUERY.DELETE_SESSION] = requestTimestamp
        return handleErrors<API_QUERY.DELETE_SESSION>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Create a new user
     * @param data
     * @param data.username The user's username
     * @param data.password The user's password
     * @returns a new user object if successful
     */
    createUser: async (data: { username: string, password: string }): Promise<API_RESPONSE[API_QUERY.POST_USER]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/users`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(removeEmpty(data)),
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.POST_USER]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.POST_USER]) {
        latestCompletedTimestamps[API_QUERY.POST_USER] = requestTimestamp
        return handleErrors<API_QUERY.POST_USER>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Get the user's information
     * @param data
     * @param data.uuid The user's uuid
     * @returns a user object if successful
     */
    getUser: async (data: { uuid: string }): Promise<API_RESPONSE[API_QUERY.GET_USER]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/users/${data.uuid}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.GET_USER]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.GET_USER]) {
        latestCompletedTimestamps[API_QUERY.GET_USER] = requestTimestamp
        return handleErrors<API_QUERY.GET_USER>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Update the user's information
     * @param data
     * @param data.username The user's new username
     * @param data.password The user's new password
     * @returns a new user object if successful
     */
    updateUser: async (data: { username?: string, password?: string }): Promise<API_RESPONSE[API_QUERY.UPDATE_USER]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/users`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(removeEmpty(data)),
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.UPDATE_USER]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.UPDATE_USER]) {
        latestCompletedTimestamps[API_QUERY.UPDATE_USER] = requestTimestamp
        return handleErrors<API_QUERY.UPDATE_USER>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Delete the user's account
     */
    deleteUser: async (): Promise<API_RESPONSE[API_QUERY.DELETE_USER]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/users`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.DELETE_USER]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.DELETE_USER]) {
        latestCompletedTimestamps[API_QUERY.DELETE_USER] = requestTimestamp
        return handleErrors<API_QUERY.DELETE_USER>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Get the user's stats
     */
    getStats: async (): Promise<API_RESPONSE[API_QUERY.GET_STATS]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/statistics`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.GET_STATS]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.GET_STATS]) {
        latestCompletedTimestamps[API_QUERY.GET_STATS] = requestTimestamp
        return handleErrors<API_QUERY.GET_STATS>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Update the user's stats
     * @param data
     * @param data.correct If the user answered correctly
     */
    updateStats: async (data: { correct: boolean }): Promise<API_RESPONSE[API_QUERY.UPDATE_STATS]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/statistics`, {
        method: 'PATCH',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(removeEmpty(data)),
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.UPDATE_STATS]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.UPDATE_STATS]) {
        latestCompletedTimestamps[API_QUERY.UPDATE_STATS] = requestTimestamp
        return handleErrors<API_QUERY.UPDATE_STATS>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Create a new question
     * @param data
     * @param data.question The question
     * @param data.difficulty The question's difficulty
     * @param data.options The question's options
     * @param data.tags The question's tags
     */
    createQuestion: async (data: { question: string, difficulty: number, options: string[], tags: number[] }): Promise<API_RESPONSE[API_QUERY.POST_QUESTION]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/questions`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(removeEmpty(data)),
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.POST_QUESTION]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.POST_QUESTION]) {
        latestCompletedTimestamps[API_QUERY.POST_QUESTION] = requestTimestamp
        return handleErrors<API_QUERY.POST_QUESTION>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Get a question
     * @param data
     * @param data.id The question's id
     */
    getQuestion: async (data: { id: number }): Promise<API_RESPONSE[API_QUERY.GET_QUESTION]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/questions/${data.id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.GET_QUESTION]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.GET_QUESTION]) {
        latestCompletedTimestamps[API_QUERY.GET_QUESTION] = requestTimestamp
        return handleErrors<API_QUERY.GET_QUESTION>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Get all questions
     */
    getQuestions: async (): Promise<API_RESPONSE[API_QUERY.GET_QUESTIONS]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/questions`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.GET_QUESTIONS]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.GET_QUESTIONS]) {
        latestCompletedTimestamps[API_QUERY.GET_QUESTIONS] = requestTimestamp
        return handleErrors<API_QUERY.GET_QUESTIONS>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Get all tags
     */
    getTags: async (): Promise<API_RESPONSE[API_QUERY.GET_TAGS]> => {
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/tags`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${session.value?.token}`,
          'Content-Type': 'application/json',
        },
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.GET_TAGS]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.GET_TAGS]) {
        latestCompletedTimestamps[API_QUERY.GET_TAGS] = requestTimestamp
        return handleErrors<API_QUERY.GET_TAGS>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
  }

  function handleErrors<T extends keyof API_RESPONSE>(response: UseFetchReturn<API_RESPONSE[T]>): API_RESPONSE[T] {
    if (response.statusCode.value === null)
      return { code: API_STATUS.TIMEOUT, message: 'Request Timed Out' }
    return response.data.value ?? { code: response.statusCode.value as API_STATUS, message: response.error.value } as API_RESPONSE[T]
  }

  function removeEmpty(obj: Record<string, any>): Record<string, any> {
    return Object.fromEntries(Object.entries(obj).filter(([_, v]) => v != null))
  }

  interface BaseAPIResponse {
    code: API_STATUS.ERROR | API_STATUS.BAD_REQUEST | API_STATUS.UNAUTHORIZED | API_STATUS.FORBIDDEN | API_STATUS.NOT_FOUND | API_STATUS.CONFLICT | API_STATUS.TIMEOUT | API_STATUS.OUTDATED | API_STATUS.OK | API_STATUS.CREATED
    message: string
  }

  interface BadAPIResponse extends BaseAPIResponse {
    code: API_STATUS.ERROR | API_STATUS.BAD_REQUEST | API_STATUS.UNAUTHORIZED | API_STATUS.FORBIDDEN | API_STATUS.NOT_FOUND | API_STATUS.CONFLICT | API_STATUS.TIMEOUT | API_STATUS.OUTDATED
  }

  interface DataAPIResponse<T> extends BaseAPIResponse {
    code: API_STATUS.OK | API_STATUS.CREATED
    message: string
    data: T
  }

  interface API_RESPONSE {
    [API_QUERY.POST_SESSION]: ExpandRecursively<DataAPIResponse<Session> | BadAPIResponse>
    [API_QUERY.DELETE_SESSION]: ExpandRecursively<BaseAPIResponse | BadAPIResponse>
    [API_QUERY.POST_USER]: ExpandRecursively<DataAPIResponse<User> | BadAPIResponse>
    [API_QUERY.GET_USER]: ExpandRecursively<DataAPIResponse<User> | BadAPIResponse>
    [API_QUERY.UPDATE_USER]: ExpandRecursively<DataAPIResponse<User> | BadAPIResponse>
    [API_QUERY.DELETE_USER]: ExpandRecursively<BaseAPIResponse | BadAPIResponse>
    [API_QUERY.POST_QUESTION]: ExpandRecursively<BaseAPIResponse | BadAPIResponse>
    [API_QUERY.GET_QUESTION]: ExpandRecursively<DataAPIResponse<Question[]> | BadAPIResponse>
    [API_QUERY.GET_QUESTIONS]: ExpandRecursively<DataAPIResponse<Question[]> | BadAPIResponse>
    [API_QUERY.GET_TAGS]: ExpandRecursively<DataAPIResponse<Tag[]> | BadAPIResponse>
    [API_QUERY.GET_STATS]: ExpandRecursively<DataAPIResponse<Stats> | BadAPIResponse>
    [API_QUERY.UPDATE_STATS]: ExpandRecursively<DataAPIResponse<Stats> | BadAPIResponse>
  }
}
