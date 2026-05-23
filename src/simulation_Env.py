from blackScholesMethods import BlackScholesMethods
import numpy as np
from scipy.stats import norm


class SimulationEnv:
    def __init__(self, S, r, K):
        self.S = S
        self.r = r
        self.K = K
    
    def volatility_arbitrage_GBM(self, n, sigma, sigma_iv, T):
        dt = T / n
        print(self.S)
        S0 = self.S
        r = self.r

        t = np.linspace(0, T, n + 1)
        dW = np.random.normal(0, np.sqrt(dt), n)
        W = np.insert(np.cumsum(dW), 0, 0)

        S = S0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)

        K = self.K  

        profit = np.zeros(n + 1)
        cumulative_profit = np.zeros(n + 1)

        # NEW: option price storage
        C_market_arr = np.zeros(n + 1)
        C_model_arr = np.zeros(n + 1)

        portfolio = (0, 0.0, 0.0)

        for i in range(n-1):
            tau = (n - i) * dt

            C_market_arr[i] = BlackScholesMethods.black_scholes_call(
                S=S[i], K=K, T=tau, r=r, sigma=sigma_iv
            )

            C_model_arr[i] = BlackScholesMethods.black_scholes_call(
                S=S[i], K=K, T=tau, r=r, sigma=sigma
            )

            if portfolio == (0, 0.0, 0.0):
                if C_market_arr[i] >= C_model_arr[i]:
                    delta = BlackScholesMethods.delta_black_scholes(
                        S=S[i], K=K, T=tau-dt, r=r, sigma=sigma
                    )
                    bond = C_market_arr[i] - delta * S[i]

                    portfolio = (-1, delta, bond)
                    profit[i] = 0

            elif portfolio[0] == -1:
                delta_old = portfolio[1]
                bond_old = portfolio[2]

                delta_new = BlackScholesMethods.delta_black_scholes(
                    S=S[i], K=K, T=tau-dt, r=r, sigma=sigma
                )

                bond_new = C_market_arr[i] - delta_new * S[i]

                change_in_option= C_market_arr[i] - C_market_arr[i-1]
                change_in_underlying= S[i] - S[i-1]
                change_in_bond= bond_old * (np.exp(r * dt) - 1)

                profit[i] = ( -change_in_option + delta_old * change_in_underlying + change_in_bond
                )

                portfolio = (-1, delta_new, bond_new)

        if portfolio[0] == -1:
            delta_old = portfolio[1]
            bond_old = portfolio[2]

            if S[-2] > K:
                delta_new = 1
            else:
                delta_new = 0

            C_market_arr[-2] = BlackScholesMethods.black_scholes_call(
                S=S[-2], K=K, T=dt, r=r, sigma=sigma_iv
            )
            bond_new = C_market_arr[-2] - delta_new * S[-2]

            change_in_option= C_market_arr[-2] - C_market_arr[-3]
            change_in_underlying= S[-2] - S[-3]
            change_in_bond= bond_old * (np.exp(r * dt) - 1)

            profit[-2] = ( -change_in_option + delta_old * change_in_underlying + change_in_bond
            )

            portfolio = (-1, delta_new, bond_new)

        if portfolio[0] == -1:
            delta_final = portfolio[1]
            bond_final = portfolio[2] * np.exp(r * dt)

            C_market_arr[-1] = max(S[-1] - K, 0)

            change_in_option= C_market_arr[-1] - C_market_arr[-2]
            change_in_underlying= S[-1] - S[-2]
            change_in_bond= bond_final * (np.exp(r * dt) - 1)

            profit[-1] = ( -change_in_option + delta_final * change_in_underlying + change_in_bond
            )


        cumulative_profit = np.cumsum(profit)


        discounted_profit = np.sum(np.exp(-r * t) * profit)

        expected_profit = (
            BlackScholesMethods.black_scholes_call(
                S=S[0], K=K, T=T, r=r, sigma=sigma_iv
            )
            - BlackScholesMethods.black_scholes_call(
                S=S[0], K=K, T=T, r=r, sigma=sigma
            )
        )

        return S, profit, cumulative_profit, discounted_profit, expected_profit
    


    def vol_arb_fast(self, n, sigma, sigma_iv,T):
        dt = T / n
        S0 = self.S
        r = self.r

        t = np.linspace(0, T, n + 1)
        dW = np.random.normal(0, np.sqrt(dt), n)
        W = np.insert(np.cumsum(dW), 0, 0)

        S = S0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)

        K = self.K  
        
        mat= np.array([T for _ in range(n+1)])

        C_Market=BlackScholesMethods.black_scholes_call(S=S[0:n], K=K, T=(mat-t)[0:n],r=r, sigma=sigma_iv)
        C_Model=BlackScholesMethods.black_scholes_call(S=S[0:n], K=K, T=(mat-t)[0:n],r=r, sigma=sigma)

        C_Market = np.concatenate((C_Market, [max(S[-1] - K, 0)]))
        C_Model = np.concatenate((C_Model, [max(S[-1] - K, 0)]))

        print(C_Market)
        print(" ")
        print(C_Model)

        expected_profit=C_Market[0]-C_Model[0]
        delta=BlackScholesMethods.delta_black_scholes(S=S[0:n-1], K=K, T=(mat-t-dt)[0:n-1],r=r, sigma=sigma)

        temp = 1 if S[-2] > K else 0
        delta = np.concatenate((delta, [temp]))

        delta = np.concatenate((delta, [0]))

        
        B=C_Market-delta*S
        profit=S[1:n+1]*(delta[0:n]-delta[1:n+1])+B[0:n]*np.exp(r*dt)-B[1:n+1]

        profit=np.concatenate(([0],profit))

        cumulative_profit = np.cumsum(profit)

        discounted_profit = np.sum(np.exp(-r * t) * profit)

        return S, B, delta, profit, cumulative_profit, discounted_profit, expected_profit, C_Market, C_Model
    

    def vol_arb_fast_matrix(self, n, N, sigma, sigma_iv,T):
        dt = T / n
        S0 = self.S
        r = self.r

        t = np.linspace(0, T, n + 1).reshape(-1, 1)
        dW = np.random.normal(0, np.sqrt(dt), (n, N))
        W = np.cumsum(dW, axis=0)
        W = np.vstack((np.zeros((1, N)), W))

        S = S0 * np.exp((r - 0.5 * sigma**2) * t + sigma * W)

        K = self.K

        C_Market = BlackScholesMethods.black_scholes_call(S=S[0:n], K=K, T=(T - t)[0:n], r=r, sigma=sigma_iv)
        C_Model = BlackScholesMethods.black_scholes_call(S=S[0:n], K=K, T=(T - t)[0:n], r=r, sigma=sigma)

        C_Market = np.concatenate((C_Market, np.maximum(S[-1] - K, 0).reshape(1, -1)), axis=0)
        C_Model = np.concatenate((C_Model, np.maximum(S[-1] - K, 0).reshape(1, -1)), axis=0)

        expected_profit=C_Market[0]-C_Model[0]
        delta=BlackScholesMethods.delta_black_scholes(S=S[0:n-1], K=K, T=(T-t-dt)[0:n-1],r=r, sigma=sigma)

        print(delta.shape)

        temp = np.where(S[-2] > K, 1, 0).reshape(1, -1)
        delta = np.concatenate((delta, temp), axis=0)

        delta = np.concatenate((delta, np.zeros((1, N))), axis=0)

        B=C_Market-delta*S
        profit=S[1:n+1]*(delta[0:n]-delta[1:n+1])+B[0:n]*np.exp(r*dt)-B[1:n+1]

        profit=np.concatenate(( np.zeros((1, N)), profit), axis=0)

        discounted_profit = np.sum(np.exp(-r * t) * profit, axis=0)

        hedging_error = discounted_profit - expected_profit

        return hedging_error, expected_profit, discounted_profit
