/**
 * @author: adibarra (Alec Ibarra)
 * @description: Composable for providing access to the QueryQuest API
 */
import type { UseFetchReturn } from '@vueuse/core'

export enum API_STATUS {
  OK = 200,
  BAD_REQUEST = 400,
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
  const API_BASE = options?.base ?? import.meta.env.DEV ? 'http://localhost:3332/api/v1' : 'https://queryquest-api.adibarra.com/api/v1'

  enum API_QUERY {
    EXAMPLE1, EXAMPLE2, EXAMPLE3,
  }

  const latestCompletedTimestamps: Record<API_QUERY, number> = {
    [API_QUERY.EXAMPLE1]: 0,
    [API_QUERY.EXAMPLE2]: 0,
    [API_QUERY.EXAMPLE3]: 0,
  }

  return {
    /**
     * Dummy example API query
     * @param data
     * @param data.query the query to send to the API
     */
    example1: async (data: { query: string }): Promise<API_RESPONSE[API_QUERY.EXAMPLE1]> => {
      const params = new URLSearchParams(removeEmpty(data))
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/example1?${params}`, {
        method: 'GET',
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.EXAMPLE1]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.EXAMPLE1]) {
        latestCompletedTimestamps[API_QUERY.EXAMPLE1] = requestTimestamp
        return handleErrors<API_QUERY.EXAMPLE1>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Dummy example API query
     * @param data
     * @param data.query the query to send to the API
     */
    example2: async (data: { query: string }): Promise<API_RESPONSE[API_QUERY.EXAMPLE2]> => {
      const params = new URLSearchParams(removeEmpty(data))
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/example2?${params}`, {
        method: 'GET',
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.EXAMPLE2]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.EXAMPLE2]) {
        latestCompletedTimestamps[API_QUERY.EXAMPLE2] = requestTimestamp
        return handleErrors<API_QUERY.EXAMPLE2>(response)
      }
      return { code: API_STATUS.OUTDATED, message: 'Request Outdated' }
    },
    /**
     * Dummy example API query
     * @param data
     * @param data.query the query to send to the API
     */
    example3: async (data: { query: string }): Promise<API_RESPONSE[API_QUERY.EXAMPLE3]> => {
      const params = new URLSearchParams(removeEmpty(data))
      const requestTimestamp = Date.now()

      const response = await useFetch(`${API_BASE}/example3?${params}`, {
        method: 'GET',
      }, { timeout: 3333 }).json<API_RESPONSE[API_QUERY.EXAMPLE3]>()

      if (requestTimestamp > latestCompletedTimestamps[API_QUERY.EXAMPLE3]) {
        latestCompletedTimestamps[API_QUERY.EXAMPLE3] = requestTimestamp
        return handleErrors<API_QUERY.EXAMPLE3>(response)
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
    code: API_STATUS.ERROR | API_STATUS.BAD_REQUEST | API_STATUS.TIMEOUT | API_STATUS.OUTDATED | API_STATUS.OK
    message: string
  }

  interface BadAPIResponse extends BaseAPIResponse {
    code: API_STATUS.ERROR | API_STATUS.BAD_REQUEST | API_STATUS.TIMEOUT | API_STATUS.OUTDATED
  }

  interface DataAPIResponse<T> extends BaseAPIResponse {
    code: API_STATUS.OK
    message: string
    data: T
  }

  interface API_RESPONSE {
    [API_QUERY.EXAMPLE1]: ExpandRecursively<DataAPIResponse<string> | BadAPIResponse>
    [API_QUERY.EXAMPLE2]: ExpandRecursively<DataAPIResponse<string> | BadAPIResponse>
    [API_QUERY.EXAMPLE3]: ExpandRecursively<DataAPIResponse<string> | BadAPIResponse>
  }
}
